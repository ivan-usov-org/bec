import { model, property } from '@loopback/repository';
import { SciBecEntity } from './scibecentity.model';

@model()
export class AccessAccount extends SciBecEntity {
  @property({
    type: 'string',
    required: true,
  })
  name: string;

  @property({
    type: 'boolean',
    required: true,
  })
  read: boolean;

  @property({
    type: 'boolean',
    required: true,
  })
  write: boolean;

  @property({
    type: 'boolean',
    required: true,
  })
  remote: boolean;

  @property({
    type: 'string',
    required: true,
  })
  token: string;

  @property({
    type: 'boolean',
    required: false,
  })
  isFunctional?: boolean;

  constructor(data?: Partial<AccessAccount>) {
    super(data);
  }
}

export interface AccessAccountRelations {
  // describe navigational properties here
}

export type AccessAccountWithRelations = AccessAccount & AccessAccountRelations;
