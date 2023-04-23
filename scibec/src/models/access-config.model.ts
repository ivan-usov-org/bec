import { belongsTo, hasMany, model, property } from '@loopback/repository';
import { Beamline } from './beamline.model';
import { FunctionalAccount } from './functional-account.model';
import { SciBecEntity } from './scibecentity.model';

@model()
export class AccessConfig extends SciBecEntity {
  @property({
    type: 'string',
  })
  targetAccount?: string;

  @belongsTo(() => Beamline,
    {}, //relation metadata goes in here
    {// property definition goes in here
      description: 'Beamline to which this config belongs.',
      mongodb: { dataType: 'ObjectId' },
      required: true,
    })
  beamlineId: string;

  @property({
    type: 'boolean',
    required: true,
  })
  authEnabled: boolean;

  @property({
    type: 'array',
    itemType: 'string',
  })
  activeAccounts?: string[];

  @hasMany(() => FunctionalAccount, { keyTo: 'accessConfigId' })
  functionalAccounts?: FunctionalAccount[];

  @property({
    type: 'boolean',
    required: true,
  })
  usePasswords: boolean;


  constructor(data?: Partial<AccessConfig>) {
    super(data);
  }
}

export interface AccessConfigRelations {
  // describe navigational properties here
}

export type AccessConfigWithRelations = AccessConfig & AccessConfigRelations;
