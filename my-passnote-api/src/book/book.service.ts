import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Book } from './book.entity';

@Injectable()
export class BookService {
  constructor(
    @InjectRepository(Book)
    private readonly bookRepository: Repository<Book>,
  ) {}

  async findBooksByCompany(company: string) {
    const raw = await this.bookRepository.query(
      `
      SELECT 
        b.title AS name,
        b.description,
        b.price,
        DATE_FORMAT(b.publication_date, '%Y-%m-%d') AS publicationDate,
        b.author,
        b.publisher,
        b.is_public AS isPublic,
        b.isbn,
        b.pages
      FROM books b
      JOIN companies c ON b.code = c.code
      WHERE c.name = ?
      ORDER BY b.created_at DESC
      `,
      [company],
    );

    return raw.map((row) => ({
      ...row,
      isPublic: !!row.isPublic,
    }));
  }

  async findPurchasesByCompany(company: string) {
    const raw = await this.bookRepository.query(
      `
      SELECT 
        b.title AS bookName,
        b.publisher,
        p.price,
        p.created_at,
        CASE WHEN p.status = 'REFUNDED' THEN 1 ELSE 0 END AS is_refunded
      FROM purchases p
      JOIN books b ON p.item_id = b.id AND p.item_type = 'BOOK'
      JOIN companies c ON b.code = c.code
      WHERE c.name = ? AND p.price != 0
      ORDER BY p.created_at DESC
      `,
      [company],
    );

    return raw.map((row) => ({
      ...row,
      created_at: new Date(row.created_at)
        .toISOString()
        .replace('T', ' ')
        .split('.')[0],
    }));
  }
}
