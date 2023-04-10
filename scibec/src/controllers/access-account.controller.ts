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
} from '@loopback/rest';
import { AccessAccount } from '../models';
import { AccessAccountRepository } from '../repositories';

export class AccessAccountController {
  constructor(
    @repository(AccessAccountRepository)
    public accessAccountRepository: AccessAccountRepository,
  ) { }

  @post('/access-accounts')
  @response(200, {
    description: 'AccessAccount model instance',
    content: { 'application/json': { schema: getModelSchemaRef(AccessAccount) } },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(AccessAccount, {
            title: 'NewAccessAccount',
            exclude: ['id'],
          }),
        },
      },
    })
    accessAccount: Omit<AccessAccount, 'id'>,
  ): Promise<AccessAccount> {
    return this.accessAccountRepository.create(accessAccount);
  }

  @get('/access-accounts/count')
  @response(200, {
    description: 'AccessAccount model count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async count(
    @param.where(AccessAccount) where?: Where<AccessAccount>,
  ): Promise<Count> {
    return this.accessAccountRepository.count(where);
  }

  @get('/access-accounts')
  @response(200, {
    description: 'Array of AccessAccount model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(AccessAccount, { includeRelations: true }),
        },
      },
    },
  })
  async find(
    @param.filter(AccessAccount) filter?: Filter<AccessAccount>,
  ): Promise<AccessAccount[]> {
    return this.accessAccountRepository.find(filter);
  }

  @patch('/access-accounts')
  @response(200, {
    description: 'AccessAccount PATCH success count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(AccessAccount, { partial: true }),
        },
      },
    })
    accessAccount: AccessAccount,
    @param.where(AccessAccount) where?: Where<AccessAccount>,
  ): Promise<Count> {
    return this.accessAccountRepository.updateAll(accessAccount, where);
  }

  @get('/access-accounts/{id}')
  @response(200, {
    description: 'AccessAccount model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(AccessAccount, { includeRelations: true }),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(AccessAccount, { exclude: 'where' }) filter?: FilterExcludingWhere<AccessAccount>
  ): Promise<AccessAccount> {
    return this.accessAccountRepository.findById(id, filter);
  }

  @patch('/access-accounts/{id}')
  @response(204, {
    description: 'AccessAccount PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(AccessAccount, { partial: true }),
        },
      },
    })
    accessAccount: AccessAccount,
  ): Promise<void> {
    await this.accessAccountRepository.updateById(id, accessAccount);
  }

  @del('/access-accounts/{id}')
  @response(204, {
    description: 'AccessAccount DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.accessAccountRepository.deleteById(id);
  }
}
