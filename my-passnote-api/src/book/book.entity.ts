import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('book')
export class Book {
  @PrimaryGeneratedColumn()
  book_id: number;

  @Column()
  name: string;

  @Column('text')
  description: string;

  @Column()
  price: number;

  @Column({ type: 'date' })
  publication_date: Date;

  @Column()
  author: string;

  @Column()
  publisher: string;

  @Column()
  isbn: string;

  @Column()
  pages: number;

  @Column({ name: 'is_public', type: 'tinyint' })
  isPublic: boolean;

  @Column()
  company_id: number;
}