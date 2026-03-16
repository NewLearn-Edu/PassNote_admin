import { Entity, Column, PrimaryColumn } from 'typeorm';

@Entity()
export class Distributor {
  @PrimaryColumn()
  distributor_id: number;

  @Column({ unique: true })
  email: string;

  @Column()
  password: string;

  @Column()
  name: string;

  @Column()
  company: string;
}