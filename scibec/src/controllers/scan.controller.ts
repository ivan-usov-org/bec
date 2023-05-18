import { inject } from '@loopback/core';
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
  getModelSchemaRef, param, patch, post, requestBody,
  response
} from '@loopback/rest';
import { Scan } from '../models';
import { ScanRepository } from '../repositories';


export interface BECMessage {
  msg_type: string,
  metadata: Object
  content: Object
}

export interface ScanQueueRequest extends BECMessage {
  content: {
    scan_type: string,
    parameter: Object,
    queue: string
  }
}

export class ScanController {
  private msgpack;

  constructor(
    @repository(ScanRepository)
    public scanRepository: ScanRepository,
  ) {
    this.msgpack = require('msgpack');

  }

  @post('/scans')
  @response(200, {
    description: 'Scan model instance',
    content: { 'application/json': { schema: getModelSchemaRef(Scan) } },
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
    let msg: ScanQueueRequest = {
      msg_type: "scan",
      content: {
        scan_type: scan.scanType,
        parameter: scan.scanParameter,
        queue: scan.queue
      },
      metadata: {
        requestID: ""
      }
    }
    return this.scanRepository.create(scan);
  }

  @get('/scans/count')
  @response(200, {
    description: 'Scan model count',
    content: { 'application/json': { schema: CountSchema } },
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
          items: getModelSchemaRef(Scan, { includeRelations: true }),
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
    content: { 'application/json': { schema: CountSchema } },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Scan, { partial: true }),
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
        schema: getModelSchemaRef(Scan, { includeRelations: true }),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(Scan, { exclude: 'where' }) filter?: FilterExcludingWhere<Scan>
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
          schema: getModelSchemaRef(Scan, { partial: true }),
        },
      },
    })
    scan: Scan,
  ): Promise<void> {
    await this.scanRepository.updateById(id, scan);
  }

  @del('/scans/{id}')
  @response(204, {
    description: 'Scan DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.scanRepository.deleteById(id);
  }
}
