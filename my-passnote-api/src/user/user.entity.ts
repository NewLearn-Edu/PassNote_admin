// src/user/user.entity.ts
import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn({ name: 'id', type: 'bigint' })
  userId: number;

  @Column({ type: 'varchar', length: 255 })
  email: string;

  @Column({ type: 'varchar', length: 255, nullable: true })
  name: string | null;

  @Column({ type: 'varchar', length: 255 })
  nickname: string;

  @Column({ type: 'varchar', length: 255 })
  target_career: string;

  @Column({ name: 'animal_type', type: 'varchar', length: 255 })
  animalType: string;

  @Column({ name: 'user_role', type: 'varchar', length: 50 })
  userRole: string;

  @Column({ type: 'varchar', length: 50 })
  status: string;

  @Column({ type: 'bigint' })
  point: number;

  @Column({ type: 'bigint' })
  reward: number;

  @Column({ type: 'timestamp' })
  created_at: Date;

  @Column({ type: 'timestamp' })
  modified_at: Date;

  @Column({ type: 'timestamp', nullable: true })
  deleted_at: Date | null;
}
