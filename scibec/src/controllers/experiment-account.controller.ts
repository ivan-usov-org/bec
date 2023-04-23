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
  put,
  del,
  requestBody,
  response,
} from '@loopback/rest';
import { ExperimentAccount } from '../models';
import { ExperimentAccountRepository } from '../repositories';

export class ExperimentAccountController {
  constructor(
    @repository(ExperimentAccountRepository)
    public experimentAccountRepository: ExperimentAccountRepository,
  ) { }

  @post('/experiment-accounts')
  @response(200, {
    description: 'ExperimentAccount model instance',
    content: { 'application/json': { schema: getModelSchemaRef(ExperimentAccount) } },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(ExperimentAccount, {
            title: 'NewExperimentAccount',
            exclude: ['id'],
          }),
        },
      },
    })
    experimentAccount: Omit<ExperimentAccount, 'id'>,
  ): Promise<ExperimentAccount> {
    return this.experimentAccountRepository.create(experimentAccount);
  }

  @get('/experiment-accounts/count')
  @response(200, {
    description: 'ExperimentAccount model count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async count(
    @param.where(ExperimentAccount) where?: Where<ExperimentAccount>,
  ): Promise<Count> {
    return this.experimentAccountRepository.count(where);
  }

  @get('/experiment-accounts')
  @response(200, {
    description: 'Array of ExperimentAccount model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(ExperimentAccount, { includeRelations: true }),
        },
      },
    },
  })
  async find(
    @param.filter(ExperimentAccount) filter?: Filter<ExperimentAccount>,
  ): Promise<ExperimentAccount[]> {
    return this.experimentAccountRepository.find(filter);
  }

  @patch('/experiment-accounts')
  @response(200, {
    description: 'ExperimentAccount PATCH success count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(ExperimentAccount, { partial: true }),
        },
      },
    })
    experimentAccount: ExperimentAccount,
    @param.where(ExperimentAccount) where?: Where<ExperimentAccount>,
  ): Promise<Count> {
    return this.experimentAccountRepository.updateAll(experimentAccount, where);
  }

  @get('/experiment-accounts/{id}')
  @response(200, {
    description: 'ExperimentAccount model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(ExperimentAccount, { includeRelations: true }),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(ExperimentAccount, { exclude: 'where' }) filter?: FilterExcludingWhere<ExperimentAccount>
  ): Promise<ExperimentAccount> {
    return this.experimentAccountRepository.findById(id, filter);
  }

  @patch('/experiment-accounts/{id}')
  @response(204, {
    description: 'ExperimentAccount PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(ExperimentAccount, { partial: true }),
        },
      },
    })
    experimentAccount: ExperimentAccount,
  ): Promise<void> {
    await this.experimentAccountRepository.updateById(id, experimentAccount);
  }

  @del('/experiment-accounts/{id}')
  @response(204, {
    description: 'ExperimentAccount DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.experimentAccountRepository.deleteById(id);
  }
}
