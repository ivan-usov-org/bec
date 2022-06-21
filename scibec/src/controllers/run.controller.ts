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
import {Run} from '../models';
import {RunRepository} from '../repositories';

export class RunController {
  constructor(
    @repository(RunRepository)
    public runRepository : RunRepository,
  ) {}

  @post('/runs')
  @response(200, {
    description: 'Run model instance',
    content: {'application/json': {schema: getModelSchemaRef(Run)}},
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Run, {
            title: 'NewRun',
            exclude: ['id'],
          }),
        },
      },
    })
    run: Omit<Run, 'id'>,
  ): Promise<Run> {
    return this.runRepository.create(run);
  }

  @get('/runs/count')
  @response(200, {
    description: 'Run model count',
    content: {'application/json': {schema: CountSchema}},
  })
  async count(
    @param.where(Run) where?: Where<Run>,
  ): Promise<Count> {
    return this.runRepository.count(where);
  }

  @get('/runs')
  @response(200, {
    description: 'Array of Run model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(Run, {includeRelations: true}),
        },
      },
    },
  })
  async find(
    @param.filter(Run) filter?: Filter<Run>,
  ): Promise<Run[]> {
    return this.runRepository.find(filter);
  }

  @patch('/runs')
  @response(200, {
    description: 'Run PATCH success count',
    content: {'application/json': {schema: CountSchema}},
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Run, {partial: true}),
        },
      },
    })
    run: Run,
    @param.where(Run) where?: Where<Run>,
  ): Promise<Count> {
    return this.runRepository.updateAll(run, where);
  }

  @get('/runs/{id}')
  @response(200, {
    description: 'Run model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(Run, {includeRelations: true}),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(Run, {exclude: 'where'}) filter?: FilterExcludingWhere<Run>
  ): Promise<Run> {
    return this.runRepository.findById(id, filter);
  }

  @patch('/runs/{id}')
  @response(204, {
    description: 'Run PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Run, {partial: true}),
        },
      },
    })
    run: Run,
  ): Promise<void> {
    await this.runRepository.updateById(id, run);
  }

  @put('/runs/{id}')
  @response(204, {
    description: 'Run PUT success',
  })
  async replaceById(
    @param.path.string('id') id: string,
    @requestBody() run: Run,
  ): Promise<void> {
    await this.runRepository.replaceById(id, run);
  }

  @del('/runs/{id}')
  @response(204, {
    description: 'Run DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.runRepository.deleteById(id);
  }
}
