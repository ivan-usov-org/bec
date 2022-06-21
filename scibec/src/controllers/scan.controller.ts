import {inject} from '@loopback/core';
import {
  Count,
  CountSchema,
  Filter,
  FilterExcludingWhere,
  repository,
  Where
} from '@loopback/repository';
import {
  del, get,
  getModelSchemaRef, param, patch, post, put, requestBody,
  response
} from '@loopback/rest';
import {
  HighLevelProducer, KafkaClient, ProduceRequest
} from 'kafka-node';
import {Scan} from '../models';
import {ScanRepository} from '../repositories';


const KAFKA_HOST = 'localhost:9092';
const KAFKA_SCAN_REQUEST_TOPIC = 'scan_queue_request';

export interface KafkaMessage {
  msg_type: string,
  metadata: Object
  content: Object
}

export interface ScanQueueRequest extends KafkaMessage {
  content: {
    scan_type: string,
    parameter: Object,
    queue: string
  }
}

export class ScanController {
  private client: KafkaClient;
  private producer: HighLevelProducer;
  private kafkaScanRequestTopic: string;
  private msgpack;

  constructor(
    @repository(ScanRepository)
    public scanRepository: ScanRepository,
    @inject('kafka.host', {optional: true})
    private kafkaHost: string = KAFKA_HOST,
    @inject('kafka.scan.request.topic', {optional: true})
    private kafkaScanRequest: string = KAFKA_SCAN_REQUEST_TOPIC,
  ) {
    this.msgpack = require('msgpack');
    this.kafkaScanRequestTopic = KAFKA_SCAN_REQUEST_TOPIC;
    this.client = new KafkaClient({kafkaHost});
    this.producer = new HighLevelProducer(this.client, {});
  }

  /**
   * Wait for the producer to be ready
   */
  private isProducerReady() {
    return new Promise<void>((resolve, reject) => {
      this.producer.on('ready', () => resolve());
      this.producer.on('error', err => reject(err));
    });
  }

  @post('/scans')
  @response(200, {
    description: 'Scan model instance',
    content: {'application/json': {schema: getModelSchemaRef(Scan)}},
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Scan, {
            title: 'NewScan',
            exclude: ['id'],
          }),
        },
      },
    })
    scan: Omit<Scan, 'id'>,
  ): Promise<Scan> {
    await this.isProducerReady();
    let topic: string = this.kafkaScanRequestTopic;
    let msg: ScanQueueRequest = {
      msg_type: "scan",
      content: {
        scan_type: scan.scanType,
        parameter: scan.parameter,
        queue: scan.queue
      },
      metadata: {
        requestID: ""
      }
    }
    let new_scan = await this.scanRepository.create(scan);
    msg.metadata = {"requestID": new_scan.id};
    const req: ProduceRequest = {topic: topic, messages: this.msgpack.pack(msg)};
    let kafka_msg = await new Promise<any>((resolve, reject) => {
      this.producer.send([req], (err, data) => {
        if (err) reject(err);
        else resolve(data);
      });
    });
    return this.scanRepository.create(scan);
  }

  @get('/scans/count')
  @response(200, {
    description: 'Scan model count',
    content: {'application/json': {schema: CountSchema}},
  })
  async count(
    @param.where(Scan) where?: Where<Scan>,
  ): Promise<Count> {
    return this.scanRepository.count(where);
  }

  @get('/scans')
  @response(200, {
    description: 'Array of Scan model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(Scan, {includeRelations: true}),
        },
      },
    },
  })
  async find(
    @param.filter(Scan) filter?: Filter<Scan>,
  ): Promise<Scan[]> {
    return this.scanRepository.find(filter);
  }

  @patch('/scans')
  @response(200, {
    description: 'Scan PATCH success count',
    content: {'application/json': {schema: CountSchema}},
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Scan, {partial: true}),
        },
      },
    })
    scan: Scan,
    @param.where(Scan) where?: Where<Scan>,
  ): Promise<Count> {
    return this.scanRepository.updateAll(scan, where);
  }

  @get('/scans/{id}')
  @response(200, {
    description: 'Scan model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(Scan, {includeRelations: true}),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(Scan, {exclude: 'where'}) filter?: FilterExcludingWhere<Scan>
  ): Promise<Scan> {
    return this.scanRepository.findById(id, filter);
  }

  @patch('/scans/{id}')
  @response(204, {
    description: 'Scan PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Scan, {partial: true}),
        },
      },
    })
    scan: Scan,
  ): Promise<void> {
    await this.scanRepository.updateById(id, scan);
  }

  @put('/scans/{id}')
  @response(204, {
    description: 'Scan PUT success',
  })
  async replaceById(
    @param.path.string('id') id: string,
    @requestBody() scan: Scan,
  ): Promise<void> {
    await this.scanRepository.replaceById(id, scan);
  }

  @del('/scans/{id}')
  @response(204, {
    description: 'Scan DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.scanRepository.deleteById(id);
  }
}
