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
import { Beamline } from '../models';
import { BeamlineRepository } from '../repositories';

export class BeamlineController {
  constructor(
    @repository(BeamlineRepository)
    public beamlineRepository: BeamlineRepository,
  ) { }

  @post('/beamlines')
  @response(200, {
    description: 'Beamline model instance',
    content: { 'application/json': { schema: getModelSchemaRef(Beamline) } },
  })
  async create(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Beamline, {
            title: 'NewBeamline',
            exclude: ['id'],
          }),
        },
      },
    })
    beamline: Omit<Beamline, 'id'>,
  ): Promise<Beamline> {
    return this.beamlineRepository.create(beamline);
  }

  @get('/beamlines/count')
  @response(200, {
    description: 'Beamline model count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async count(
    @param.where(Beamline) where?: Where<Beamline>,
  ): Promise<Count> {
    return this.beamlineRepository.count(where);
  }

  @get('/beamlines')
  @response(200, {
    description: 'Array of Beamline model instances',
    content: {
      'application/json': {
        schema: {
          type: 'array',
          items: getModelSchemaRef(Beamline, { includeRelations: true }),
        },
      },
    },
  })
  async find(
    @param.filter(Beamline) filter?: Filter<Beamline>,
  ): Promise<Beamline[]> {
    return this.beamlineRepository.find(filter);
  }

  @patch('/beamlines')
  @response(200, {
    description: 'Beamline PATCH success count',
    content: { 'application/json': { schema: CountSchema } },
  })
  async updateAll(
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Beamline, { partial: true }),
        },
      },
    })
    beamline: Beamline,
    @param.where(Beamline) where?: Where<Beamline>,
  ): Promise<Count> {
    return this.beamlineRepository.updateAll(beamline, where);
  }

  @get('/beamlines/{id}')
  @response(200, {
    description: 'Beamline model instance',
    content: {
      'application/json': {
        schema: getModelSchemaRef(Beamline, { includeRelations: true }),
      },
    },
  })
  async findById(
    @param.path.string('id') id: string,
    @param.filter(Beamline, { exclude: 'where' }) filter?: FilterExcludingWhere<Beamline>
  ): Promise<Beamline> {
    return this.beamlineRepository.findById(id, filter);
  }

  @patch('/beamlines/{id}')
  @response(204, {
    description: 'Beamline PATCH success',
  })
  async updateById(
    @param.path.string('id') id: string,
    @requestBody({
      content: {
        'application/json': {
          schema: getModelSchemaRef(Beamline, { partial: true }),
        },
      },
    })
    beamline: Beamline,
  ): Promise<void> {
    await this.beamlineRepository.updateById(id, beamline);
  }

  @del('/beamlines/{id}')
  @response(204, {
    description: 'Beamline DELETE success',
  })
  async deleteById(@param.path.string('id') id: string): Promise<void> {
    await this.beamlineRepository.deleteById(id);
  }
}
