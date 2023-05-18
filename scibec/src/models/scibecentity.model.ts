import { Entity, model, property } from '@loopback/repository';

@model()
export class SciBecEntity extends Entity {
  @property({
    type: 'string',
    id: true,
    generated: true,
  })
  id?: string;

  @property.array(String, {
    description: 'groups or users who can create subentries',
    index: true,
  })
  createACL: string[];

  @property.array(String, {
    description: 'groups or users who can read this entry',
    index: true,
  })
  readACL: string[];

  @property.array(String, {
    description: 'groups or users who can update this entry',
    index: true,
  })
  updateACL: string[];

  @property.array(String, {
    description: 'groups or users who can delete this entry',
    index: true,
  })
  deleteACL: string[];

  @property.array(String, {
    description: 'groups or users who can add users/groups to createACL, readACL and updateACL',
    index: true,
  })
  shareACL: string[];

  @property.array(String, {
    description: 'groups or users who can administrate this entry',
    index: true,
  })
  adminACL: string[];

  @property({
    type: 'date',
  })
  createdAt: Date;

  @property({
    type: 'string',
  })
  createdBy: string;


  constructor(data?: Partial<SciBecEntity>) {
    super(data);
  }
}

export interface SciBecEntityRelations {
  // describe navigational properties here
}

export type SciBecEntityWithRelations = SciBecEntity & SciBecEntityRelations;
