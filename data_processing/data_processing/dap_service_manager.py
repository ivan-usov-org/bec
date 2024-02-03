from __future__ import annotations

import inspect

from bec_lib import BECClient, MessageEndpoints, bec_logger, messages
from bec_lib.lmfit_serializer import serialize_lmfit_params
from bec_lib.redis_connector import MessageObject
from bec_lib.signature_serializer import signature_to_dict

from data_processing import dap_service as dap_plugins

logger = bec_logger.logger


class DAPServiceManager:
    """Base class for data processing services."""

    def __init__(self) -> None:
        self.connector = None
        self.producer = None
        self._started = False
        self.client = None
        self._dap_request_thread = None
        self.available_dap_services = {}
        self.dap_services = {}
        self.continuous_dap = None

    def _start_dap_request_consumer(self) -> None:
        """
        Start the dap request consumer.
        """
        self._dap_request_thread = self.connector.consumer(
            topics=MessageEndpoints.dap_request(), cb=self._dap_request_callback, parent=self
        )
        self._dap_request_thread.start()

    @staticmethod
    def _dap_request_callback(msg: MessageObject, *, parent: DAPServiceManager) -> None:
        """
        Callback function for dap request consumer.

        Args:
            msg (MessageObject): MessageObject instance
            parent (DAPService): DAPService instance
        """
        dap_request_msg = messages.DAPRequestMessage.loads(msg.value)
        if not dap_request_msg:
            return
        parent.process_dap_request(dap_request_msg)

    def process_dap_request(self, dap_request_msg: messages.DAPRequestMessage) -> None:
        """
        Process a dap request.

        Args:
            dap_request_msg (DAPRequestMessage): DAPRequestMessage instance
        """
        logger.info(f"Processing dap request {dap_request_msg}")
        try:
            dap_cls = self._get_dap_cls(dap_request_msg)
            dap_type = dap_request_msg.content["dap_type"]
            result = None
            if dap_type == "continuous":
                self._start_continuous_dap(dap_cls, dap_request_msg)
            elif dap_type == "on_demand":
                result = self._start_on_demand_dap(dap_cls, dap_request_msg)
            else:
                raise ValueError(f"Unknown dap type {dap_type}")

        # pylint: disable=broad-except
        except Exception as e:
            logger.exception(f"Failed to process dap request {dap_request_msg}: {e}")
            self.send_dap_response(
                dap_request_msg, success=False, error=str(e), metadata=dap_request_msg.metadata
            )
            return

        self.send_dap_response(
            dap_request_msg, success=True, data=result, metadata=dap_request_msg.metadata
        )

    def _start_continuous_dap(
        self, dap_cls: type, dap_request_msg: messages.DAPRequestMessage
    ) -> None:
        if not self.client:
            return
        if self.continuous_dap is not None:
            self.client.callbacks.remove(self.continuous_dap["id"])

        dap_config = dap_request_msg.content["config"]
        if not dap_config.get("auto_fit"):
            return

        config = dap_request_msg.content["config"]
        cls_args = config["class_args"]
        cls_kwargs = config["class_kwargs"]
        dap_instance = dap_cls(*cls_args, client=self.client, **cls_kwargs, continuous=True)
        dap_instance.configure(**dap_config)
        self.continuous_dap = {
            "id": self.client.callbacks.register(
                # pylint: disable=protected-access
                event_type="scan_status",
                callback=dap_instance._process_scan_status_update,
            ),
            "instance": dap_instance,
        }

    def _start_on_demand_dap(
        self, dap_cls: type, dap_request_msg: messages.DAPRequestMessage
    ) -> dict:
        """
        Start an on demand dap.
        """
        config = dap_request_msg.content["config"]
        cls_args = config["class_args"]
        cls_kwargs = config["class_kwargs"]
        dap_instance = dap_cls(*cls_args, client=self.client, **cls_kwargs)
        config = dap_request_msg.content["config"]
        dap_instance.configure(*config["args"], **config["kwargs"])
        result = dap_instance.process()
        return result

    def _get_dap_cls(self, dap_request_msg: messages.DAPRequestMessage) -> type:
        """
        Get the dap class.

        Args:
            dap_request_msg (DAPRequestMessage): DAPRequestMessage instance

        Returns:
            type: DAP class
        """
        dap_cls = dap_request_msg.content["dap_cls"]
        if dap_cls in self.dap_services:
            return self.dap_services[dap_cls]
        raise ValueError(f"Unknown dap class {dap_cls}")

    def send_dap_response(
        self,
        dap_request_msg: messages.DAPRequestMessage,
        success: bool,
        data=None,
        error: str = None,
        metadata: dict = None,
    ) -> None:
        """
        Send a dap response.

        Args:
            dap_request_msg (DAPRequestMessage): DAPRequestMessage instance
            success (bool): Success flag
            error (str, optional): Error message. Defaults to None.
            data (dict, optional): Data. Defaults to None.
            metadata (dict, optional): Metadata. Defaults to None.
        """
        dap_response_msg = messages.DAPResponseMessage(
            success=success,
            data=data,
            error=error,
            dap_request=dap_request_msg.dumps(),
            metadata=metadata,
        )
        self.producer.set_and_publish(
            MessageEndpoints.dap_response(metadata.get("RID")), dap_response_msg.dumps(), expire=60
        )

    def start(self, client: BECClient) -> None:
        """
        Start the data processing service.

        Args:
            connector (RedisConnector): RedisConnector instance
        """
        if self._started:
            return
        self.client = client
        self.connector = client.connector
        self.producer = self.connector.producer()
        self._start_dap_request_consumer()
        self.update_available_dap_services()
        self.publish_available_services()

    def update_available_dap_services(self):
        """
        Update the available dap services.
        """
        members = inspect.getmembers(dap_plugins)

        for name, service_cls in members:
            if name in ["DAPServiceBase", "LmfitService"]:
                continue
            try:
                is_service = issubclass(service_cls, dap_plugins.DAPServiceBase)
            except TypeError:
                is_service = False

            if not is_service:
                logger.debug(f"Ignoring {name}")
                continue
            if name in self.available_dap_services:
                logger.error(f"{service_cls.scan_name} already exists. Skipping.")
                continue

            self.dap_services[name] = service_cls
            if hasattr(service_cls, "available_models"):
                services = {
                    model.__name__: {
                        "class": name,
                        "user_friendly_name": model.__name__,
                        "doc": service_cls.configure.__doc__ or service_cls.__init__.__doc__,
                        "signature": signature_to_dict(service_cls.configure),
                        "auto_fit_supported": getattr(service_cls, "AUTO_FIT_SUPPORTED", False),
                        "params": serialize_lmfit_params(
                            service_cls.get_model(model)().make_params()
                        ),
                        "class_args": [],
                        "class_kwargs": {"model": model.__name__},
                    }
                    for model in service_cls.available_models()
                }

                self.available_dap_services.update(services)
            else:
                self.available_dap_services[name] = {
                    "class": name,
                    "user_friendly_name": name,
                    "doc": service_cls.__doc__ or service_cls.__init__.__doc__,
                    "signature": signature_to_dict(service_cls.configure),
                    "params": serialize_lmfit_params(service_cls.get_model().make_params()),
                    "auto_fit_supported": getattr(service_cls, "AUTO_FIT_SUPPORTED", False),
                }

    def publish_available_services(self):
        """send all available dap services to the broker"""
        msg = messages.AvailableResourceMessage(resource=self.available_dap_services).dumps()
        self.producer.set(MessageEndpoints.dap_available_plugins(), msg)
