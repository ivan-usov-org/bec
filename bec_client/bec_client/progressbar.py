import asyncio
import time
from typing import Any, Callable, List

import numpy as np
import rich.progress
from rich.text import Text


class MoveTaskProgressColumn(rich.progress.TaskProgressColumn):
    def render(self, task) -> Text:
        if task.total is None and self.show_speed:
            return self.render_speed(task.finished_speed or task.speed)
        if task.fields.get("fields"):
            _text = f"[progress.percentage]{task.fields['fields'].get('current_pos'):10.2f} / {task.percentage:>3.0f} %"
        else:
            _text = f"[progress.percentage]{task.percentage:>3.0f}%s"
        if self.markup:
            text = Text.from_markup(_text, style=self.style, justify=self.justify)
        else:
            text = Text(_text, style=self.style, justify=self.justify)
        if self.highlighter:
            self.highlighter.highlight(text)
        return text


class DeviceProgressBar:
    NUM_STEPS = 1000
    UPDATE_FREQUENCY = 10

    def __init__(
        self,
        devices: List[str],
        target_values: List[float],
        start_values: List[float] = None,
        clear_on_exit: bool = False,
    ) -> None:
        self.clear_on_exit = clear_on_exit
        self.target_values = target_values
        self.start_values = start_values
        self.devices = devices

        self._progress = None
        self._tasks = []
        self._columns = (
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.BarColumn(),
            MoveTaskProgressColumn(),
            rich.progress.TimeRemainingColumn(),
            rich.progress.TimeElapsedColumn(),
        )

    def _init_tasks(self):
        for ii, dev in enumerate(self.devices):
            self._tasks.append(
                self._progress.add_task(
                    f"[green] {dev}:{self.start_values[ii]:10.2f}", total=self.NUM_STEPS
                )
            )

    def _update_task(self, device_index: int, task: Any, value: float) -> None:
        if not self._progress.tasks[task].finished:
            movement_range = self.target_values[device_index] - self.start_values[device_index]
            if np.abs(movement_range) > 0:
                completed = np.abs(
                    (value - self.start_values[device_index]) / movement_range * self.NUM_STEPS
                )
            else:
                completed = self.NUM_STEPS
            self._progress.update(
                task,
                completed=completed,
                fields={"current_pos": value, "target_pos": self.target_values[device_index]},
            )

    def start(self) -> None:
        self._progress = rich.progress.Progress(*self._columns, transient=self.clear_on_exit)
        self._progress.start()
        self._init_tasks()

    @property
    def finished(self):
        return self._progress.finished

    def set_finished(self, device):
        device_index = self.devices.index(device)
        self._progress.tasks[self._tasks[device_index]].finished = True

    def update(self, values):
        for ii, task in enumerate(self._tasks):
            self._update_task(device_index=ii, task=task, value=values[ii])

    async def sleep(self):
        await asyncio.sleep(1 / self.UPDATE_FREQUENCY)

    def stop(self) -> None:
        self._progress.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


if __name__ == "__main__":

    devices = ["samx", "samy"]
    target_values = [25, 50]
    start = [0, 5]
    steps_sim = []
    for ii, dev in enumerate(devices):
        steps_sim.append(np.linspace(start[ii], target_values[ii], 100 * (ii + 1)))
    loop_index = 0

    def get_device_values(index):
        values = [
            steps_sim[dev_index][min(index, len(steps_sim[dev_index]) - 1)]
            for dev_index, _ in enumerate(devices)
        ]
        return values

    with DeviceProgressBar(
        devices=devices, start_values=start, target_values=target_values
    ) as progress:
        while not progress.finished:
            values = get_device_values(loop_index)
            progress.update(values=values)
            time.sleep(0.001)
            # for ii, dev in enumerate(devices):
            #     if np.isclose(values[ii], target_values[ii], atol=0.05):
            #         progress.set_finished(dev)
            loop_index += 1
