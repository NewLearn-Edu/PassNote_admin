import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class Template {
  @PrimaryGeneratedColumn()
  template_id: number;

  @Column()
  name: string;

  @Column()
  price: string;

  @Column({ type: 'datetime' })
  created_at: Date;

  @Column()
  category: string;

  @Column()
  seller: string;

  @Column({ name: 'is_public', type: 'bool', default: true })
  isPublic: boolean;
}