import { hasMany, hasOne, model, property } from '@loopback/repository';
import { AccessConfig } from './access-config.model';
import { Experiment } from './experiment.model';
import { SciBecEntity } from './scibecentity.model';

@model()
export class Beamline extends SciBecEntity {

  @property({
    type: 'string',
    required: true,
  })
  name: string;

  @hasOne(() => AccessConfig, { keyTo: 'beamlineId' })
  accessConfig?: AccessConfig;

  @hasMany(() => Experiment, { keyTo: 'beamlineId' })
  experiments?: Experiment[];

  @property({
    type: 'string',
  })
  activeExperiment?: string;

  constructor(data?: Partial<Beamline>) {
    super(data);
  }
}

export interface BeamlineRelations {
  // describe navigational properties here
}

export type BeamlineWithRelations = Beamline & BeamlineRelations;
