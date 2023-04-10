import { hasMany, model, property } from '@loopback/repository';
import { AccessAccount } from './access-account.model';
import { ExperimentAccount } from './experiment-account.model';
import { SciBecEntity } from './scibecentity.model';
import { Session } from './session.model';

@model()
export class Experiment extends SciBecEntity {
  @property({
    type: 'string',
    required: true,
  })
  name: string;

  @property({
    type: 'array',
    itemType: 'string',
  })
  datasets?: string[];

  @property({
    type: 'string',
    required: true,
  })
  beamlineId: string;

  @property({
    type: 'string',
  })
  writeAccount: string;

  @hasMany(() => ExperimentAccount, { keyTo: 'experimentId' })
  experimentAccounts?: ExperimentAccount[];

  @property({
    type: 'string',
  })
  userId?: string;

  @property({
    type: 'string',
  })
  logbook?: string;

  @property({
    type: 'array',
    itemType: 'string',
  })
  samples?: string[];

  @property({
    type: 'object',
  })
  experimentConfig?: object;

  @property({
    type: 'object',
  })
  experimentInfo?: object;

  @property({
    type: 'string',
  })
  activeSession?: string;

  @hasMany(() => Session, { keyTo: 'experimentId' })
  sessions?: Session[];

  constructor(data?: Partial<Experiment>) {
    super(data);
  }
}

export interface ExperimentRelations {
  // describe navigational properties here
}

export type ExperimentWithRelations = Experiment & ExperimentRelations;
