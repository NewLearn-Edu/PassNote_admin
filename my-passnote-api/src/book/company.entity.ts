import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('company')
export class Company {
  @PrimaryGeneratedColumn()
  company_id: number;

  @Column()
  name: string;

  @Column()
  type: string;
}