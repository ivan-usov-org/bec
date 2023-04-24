import { belongsTo, hasMany, model, property } from '@loopback/repository';
import { Device, Experiment, Scan } from '.';
import { SciBecEntity } from './scibecentity.model';

@model()
export class Session extends SciBecEntity {

  @property({
    type: 'string',
    required: true,
  })
  name?: string;

  // @property({
  //   type: 'string',
  //   required: true,
  // })
  // experimentId: string;

  @belongsTo(() => Experiment,
    {}, //relation metadata goes in here
    {// property definition goes in here
      description: 'Session to which this device belongs.',
      mongodb: { dataType: 'ObjectId' }
    })
  experimentId?: string;

  @hasMany(() => Scan, { keyTo: 'sessionId' })
  scans?: Scan[];

  @hasMany(() => Device, { keyTo: 'sessionId' })
  devices?: Device[];

  @property({
    type: 'object',
  })
  sessionConfig?: object;

  constructor(data?: Partial<Session>) {
    super(data);
  }
}

export interface SessionRelations {
  // describe navigational properties here
}

export type SessionWithRelations = Session & SessionRelations;
