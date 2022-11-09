import { Entity, hasMany, model, property } from '@loopback/repository';
import { Session } from './session.model';

@model()
export class Beamline extends Entity {
  @property({
    type: 'string',
    id: true,
    generated: true,
  })
  id?: string;

  @property({
    type: 'string',
    required: true,
  })
  name: string;

  @property({
    type: 'string',
  })
  ownerGroup?: string;

  @property({
    type: 'array',
    itemType: 'string',
  })
  accessGroups?: string[];

  @property({
    type: 'date',
  })
  createdAt: Date;

  @property({
    type: 'string',
  })
  createdBy: string;

  @property({
    type: 'string',
  })
  activeSession?: string;

  @hasMany(() => Session, { keyTo: 'beamlineId' })
  sessions?: Session[];


  constructor(data?: Partial<Beamline>) {
    super(data);
  }
}

export interface BeamlineRelations {
  // describe navigational properties here
}

export type BeamlineWithRelations = Beamline & BeamlineRelations;
