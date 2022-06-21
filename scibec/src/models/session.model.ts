import {Entity, hasMany, model, property} from '@loopback/repository';
import {Device, Scan} from '.';

@model()
export class Session extends Entity {
  @property({
    type: 'string',
    id: true,
    generated: true,
  })
  id?: string;

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
    required: true,
  })
  name?: string;

  @hasMany(() => Scan, {keyTo: 'sessionId'})
  scans?: Scan[];

  @hasMany(() => Device, {keyTo: 'sessionId'})
  devices?: Device[];

  // @belongsTo(() => Session,
  //   {}, //relation metadata goes in here
  //   {// property definition goes in here
  //     mongodb: {dataType: 'ObjectId'}
  //   })
  // sessionId?: string;

  constructor(data?: Partial<Session>) {
    super(data);
  }
}

export interface SessionRelations {
  // describe navigational properties here
}

export type SessionWithRelations = Session & SessionRelations;
