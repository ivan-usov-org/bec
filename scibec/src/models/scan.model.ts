import {belongsTo, Entity, hasMany, model, property} from '@loopback/repository';
import {Dataset, DatasetWithRelations, Session, SessionWithRelations} from '.';

@model()
export class Scan extends Entity {
  @property({
    type: 'string',
    id: true,
    generated: true,
    mongodb: {datatype: 'ObjectId'}
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
    type: 'date',
  })
  updatedAt: Date;

  @property({
    type: 'string',
  })
  updatedBy: string;

  @property({
    type: 'string',
  })
  scanType: string;

  @property({
    type: 'string',
    default: "primary"
  })
  queue: string;

  @property({
    type: 'object',
  })
  parameter: Object;

  @belongsTo(() => Session,
    {}, //relation metadata goes in here
    {// property definition goes in here
      mongodb: {dataType: 'ObjectId'}
    })
  sessionId?: string;

  @hasMany(() => Dataset, {keyTo: 'scanId'})
  datasets?: Dataset[];

  @hasMany(() => Scan, {keyTo: 'parentId'})
  subscans?: Scan[];

  @belongsTo(() => Scan,
    {}, //relation metadata goes in here
    {// property definition goes in here
      mongodb: {dataType: 'ObjectId'}
    })
  parentId?: string;

  // @belongsTo(() => Session,
  //   {}, //relation metadata goes in here
  //   {// property definition goes in here
  //     mongodb: {dataType: 'ObjectId'}
  //   })
  // sessionId?: string;


  constructor(data?: Partial<Scan>) {
    super(data);
  }
}

export interface ScanRelations {
  // describe navigational properties here
  session?: SessionWithRelations;
  datasets?: DatasetWithRelations[];
  subscans?: ScanWithRelations[];
  parent?: ScanWithRelations;
}

export type ScanWithRelations = Scan & ScanRelations;
