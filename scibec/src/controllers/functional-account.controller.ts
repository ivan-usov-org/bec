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
import { FunctionalAccount } from '../models';
import { FunctionalAccountRepository } from '../repositories';

export class FunctionalAccountController {
  constructor(
    @repository(FunctionalAccountRepository)
    public functionalAccountRepository: FunctionalAccountRepository,
  ) { }

  @post('/functional-accounts')
  @response(200, {
    description: 'FunctionalAccount model instance',
    content: { 'application/json': { schema: getModelSchemaRef(FunctionalAccount) } },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(FunctionalAccount, {
            title: 'NewFunctionalAccount',
            exclude: ['id'],
          }),
        },
      },
    })
    functionalAccount: Omit<FunctionalAccount, 'id'>,
  ): Promise<FunctionalAccount> {
    return this.functionalAccountRepository.create(functionalAccount);
  }

  @get('/functional-accounts/count')
  @response(200, {
    description: 'FunctionalAccount model count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async count(
    @param.where(FunctionalAccount) where?: Where<FunctionalAccount>,
  ): Promise<Count> {
    return this.functionalAccountRepository.count(where);
  }

  @get('/functional-accounts')
  @response(200, {
    description: 'Array of FunctionalAccount model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(FunctionalAccount, { includeRelations: true }),
        },
      },
    },
  })
  async find(
    @param.filter(FunctionalAccount) filter?: Filter<FunctionalAccount>,
  ): Promise<FunctionalAccount[]> {
    return this.functionalAccountRepository.find(filter);
  }

  @patch('/functional-accounts')
  @response(200, {
    description: 'FunctionalAccount PATCH success count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(FunctionalAccount, { partial: true }),
        },
      },
    })
    functionalAccount: FunctionalAccount,
    @param.where(FunctionalAccount) where?: Where<FunctionalAccount>,
  ): Promise<Count> {
    return this.functionalAccountRepository.updateAll(functionalAccount, where);
  }

  @get('/functional-accounts/{id}')
  @response(200, {
    description: 'FunctionalAccount model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(FunctionalAccount, { includeRelations: true }),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(FunctionalAccount, { exclude: 'where' }) filter?: FilterExcludingWhere<FunctionalAccount>
  ): Promise<FunctionalAccount> {
    return this.functionalAccountRepository.findById(id, filter);
  }

  @patch('/functional-accounts/{id}')
  @response(204, {
    description: 'FunctionalAccount PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(FunctionalAccount, { partial: true }),
        },
      },
    })
    functionalAccount: FunctionalAccount,
  ): Promise<void> {
    await this.functionalAccountRepository.updateById(id, functionalAccount);
  }

  @del('/functional-accounts/{id}')
  @response(204, {
    description: 'FunctionalAccount DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.functionalAccountRepository.deleteById(id);
  }
}
