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
import { Experiment } from '../models';
import { ExperimentRepository } from '../repositories';

export class ExperimentController {
  constructor(
    @repository(ExperimentRepository)
    public experimentRepository: ExperimentRepository,
  ) { }

  @post('/experiments')
  @response(200, {
    description: 'Experiment model instance',
    content: { 'application/json': { schema: getModelSchemaRef(Experiment) } },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Experiment, {
            title: 'NewExperiment',
            exclude: ['id'],
          }),
        },
      },
    })
    experiment: Omit<Experiment, 'id'>,
  ): Promise<Experiment> {
    return this.experimentRepository.create(experiment);
  }

  @get('/experiments/count')
  @response(200, {
    description: 'Experiment model count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async count(
    @param.where(Experiment) where?: Where<Experiment>,
  ): Promise<Count> {
    return this.experimentRepository.count(where);
  }

  @get('/experiments')
  @response(200, {
    description: 'Array of Experiment model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(Experiment, { includeRelations: true }),
        },
      },
    },
  })
  async find(
    @param.filter(Experiment) filter?: Filter<Experiment>,
  ): Promise<Experiment[]> {
    return this.experimentRepository.find(filter);
  }

  @patch('/experiments')
  @response(200, {
    description: 'Experiment PATCH success count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Experiment, { partial: true }),
        },
      },
    })
    experiment: Experiment,
    @param.where(Experiment) where?: Where<Experiment>,
  ): Promise<Count> {
    return this.experimentRepository.updateAll(experiment, where);
  }

  @get('/experiments/{id}')
  @response(200, {
    description: 'Experiment model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(Experiment, { includeRelations: true }),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(Experiment, { exclude: 'where' }) filter?: FilterExcludingWhere<Experiment>
  ): Promise<Experiment> {
    return this.experimentRepository.findById(id, filter);
  }

  @patch('/experiments/{id}')
  @response(204, {
    description: 'Experiment PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Experiment, { partial: true }),
        },
      },
    })
    experiment: Experiment,
  ): Promise<void> {
    await this.experimentRepository.updateById(id, experiment);
  }

  @del('/experiments/{id}')
  @response(204, {
    description: 'Experiment DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.experimentRepository.deleteById(id);
  }
}
