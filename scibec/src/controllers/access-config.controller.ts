import {
  Count,
  CountSchema,
  Filter,
  FilterExcludingWhere,
  repository,
  Where,
} from '@loopback/repository';
import {
  post,
  param,
  get,
  getModelSchemaRef,
  patch,
  del,
  requestBody,
  response,
  HttpErrors,
} from '@loopback/rest';
import { AccessConfig } from '../models';
import { AccessConfigRepository } from '../repositories';

export class AccessConfigController {
  constructor(
    @repository(AccessConfigRepository)
    public accessConfigRepository: AccessConfigRepository,
  ) { }

  @post('/access-configs')
  @response(200, {
    description: 'AccessConfig model instance',
    content: { 'application/json': { schema: getModelSchemaRef(AccessConfig) } },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(AccessConfig, {
            title: 'NewAccessConfig',
            exclude: ['id'],
          }),
        },
      },
    })
    accessConfig: Omit<AccessConfig, 'id'>,
  ): Promise<AccessConfig> {
    if (accessConfig.beamlineId) {
      let existingData = await this.accessConfigRepository.findOne({ "where": { "beamlineId": accessConfig.beamlineId } });
      if (existingData) {
        throw new HttpErrors.Conflict('The beamline has an access config already defined.');
      }
    }

    return this.accessConfigRepository.create(accessConfig);
  }

  @get('/access-configs/count')
  @response(200, {
    description: 'AccessConfig model count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async count(
    @param.where(AccessConfig) where?: Where<AccessConfig>,
  ): Promise<Count> {
    return this.accessConfigRepository.count(where);
  }

  @get('/access-configs')
  @response(200, {
    description: 'Array of AccessConfig model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(AccessConfig, { includeRelations: true }),
        },
      },
    },
  })
  async find(
    @param.filter(AccessConfig) filter?: Filter<AccessConfig>,
  ): Promise<AccessConfig[]> {
    return this.accessConfigRepository.find(filter);
  }

  @patch('/access-configs')
  @response(200, {
    description: 'AccessConfig PATCH success count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(AccessConfig, { partial: true }),
        },
      },
    })
    accessConfig: AccessConfig,
    @param.where(AccessConfig) where?: Where<AccessConfig>,
  ): Promise<Count> {
    return this.accessConfigRepository.updateAll(accessConfig, where);
  }

  @get('/access-configs/{id}')
  @response(200, {
    description: 'AccessConfig model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(AccessConfig, { includeRelations: true }),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(AccessConfig, { exclude: 'where' }) filter?: FilterExcludingWhere<AccessConfig>
  ): Promise<AccessConfig> {
    return this.accessConfigRepository.findById(id, filter);
  }

  @patch('/access-configs/{id}')
  @response(204, {
    description: 'AccessConfig PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(AccessConfig, { partial: true }),
        },
      },
    })
    accessConfig: AccessConfig,
  ): Promise<void> {
    await this.accessConfigRepository.updateById(id, accessConfig);
  }

  @del('/access-configs/{id}')
  @response(204, {
    description: 'AccessConfig DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.accessConfigRepository.deleteById(id);
  }
}
