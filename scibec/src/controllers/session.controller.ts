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
import {Session} from '../models';
import {SessionRepository} from '../repositories';

export class SessionController {
  constructor(
    @repository(SessionRepository)
    public sessionRepository : SessionRepository,
  ) {}

  @post('/sessions')
  @response(200, {
    description: 'Session model instance',
    content: {'application/json': {schema: getModelSchemaRef(Session)}},
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Session, {
            title: 'NewSession',
            exclude: ['id'],
          }),
        },
      },
    })
    session: Omit<Session, 'id'>,
  ): Promise<Session> {
    return this.sessionRepository.create(session);
  }

  @get('/sessions/count')
  @response(200, {
    description: 'Session model count',
    content: {'application/json': {schema: CountSchema}},
  })
  async count(
    @param.where(Session) where?: Where<Session>,
  ): Promise<Count> {
    return this.sessionRepository.count(where);
  }

  @get('/sessions')
  @response(200, {
    description: 'Array of Session model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(Session, {includeRelations: true}),
        },
      },
    },
  })
  async find(
    @param.filter(Session) filter?: Filter<Session>,
  ): Promise<Session[]> {
    return this.sessionRepository.find(filter);
  }

  @patch('/sessions')
  @response(200, {
    description: 'Session PATCH success count',
    content: {'application/json': {schema: CountSchema}},
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Session, {partial: true}),
        },
      },
    })
    session: Session,
    @param.where(Session) where?: Where<Session>,
  ): Promise<Count> {
    return this.sessionRepository.updateAll(session, where);
  }

  @get('/sessions/{id}')
  @response(200, {
    description: 'Session model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(Session, {includeRelations: true}),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(Session, {exclude: 'where'}) filter?: FilterExcludingWhere<Session>
  ): Promise<Session> {
    return this.sessionRepository.findById(id, filter);
  }

  @patch('/sessions/{id}')
  @response(204, {
    description: 'Session PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Session, {partial: true}),
        },
      },
    })
    session: Session,
  ): Promise<void> {
    await this.sessionRepository.updateById(id, session);
  }

  @put('/sessions/{id}')
  @response(204, {
    description: 'Session PUT success',
  })
  async replaceById(
    @param.path.string('id') id: string,
    @requestBody() session: Session,
  ): Promise<void> {
    await this.sessionRepository.replaceById(id, session);
  }

  @del('/sessions/{id}')
  @response(204, {
    description: 'Session DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.sessionRepository.deleteById(id);
  }
}
