import { belongsTo, model, property } from '@loopback/repository';
import { AccessAccount } from './access-account.model';
import { AccessConfig } from './access-config.model';

@model({
  settings: {
    strict: false,
    scope: {
      where: { isFunctional: true },
    },
    mongodb: { collection: 'AccessAccount' },
  },
})
export class FunctionalAccount extends AccessAccount {

  @property({
    type: 'boolean',
    default: true,
  })
  isFunctional: boolean;

  @belongsTo(() => AccessConfig,
    {}, //relation metadata goes in here
    {// property definition goes in here
      description: 'AccessConfig to which this account belongs.',
      mongodb: { dataType: 'ObjectId' }
    })
  accessConfigId?: string;

  constructor(data?: Partial<FunctionalAccount>) {
    super(data);
  }
}

export interface FunctionalAccountRelations {
  // describe navigational properties here
}

export type FunctionalAccountWithRelations = FunctionalAccount & FunctionalAccountRelations;
