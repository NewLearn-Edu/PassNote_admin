import { Injectable, ForbiddenException } from '@nestjs/common';
import { DataSource } from 'typeorm';

@Injectable()
export class AdminService {
  constructor(private dataSource: DataSource) {}

  async getStatistics(user: any) {
    if (user.type !== 'admin') {
      throw new ForbiddenException();
    }

    const totalUsers = await this.dataSource.query(
      'SELECT COUNT(*) AS total FROM users',
    );
    const currentUsers = await this.dataSource.query(
      'SELECT COUNT(*) AS total FROM users WHERE deleted_at IS NULL',
    );
    const deletedUsers = await this.dataSource.query(
      'SELECT COUNT(*) AS total FROM users WHERE deleted_at IS NOT NULL',
    );
    const totalBooks = await this.dataSource.query(
      'SELECT COUNT(*) AS total FROM books WHERE is_public = 1',
    );
    const totalTemplates = await this.dataSource.query(
      'SELECT COUNT(*) AS total FROM templates WHERE is_public = 1',
    );

    const totalBookSales = await this.dataSource.query(
      'SELECT SUM(price) AS total FROM purchases WHERE item_type="BOOK"',
    );
    const totalTemplateSales = await this.dataSource.query(
      'SELECT SUM(price) AS total FROM purchases WHERE item_type="TEMPLATE"',
    );

    const bookSalesByCompany = await this.dataSource.query(`
      SELECT b.publisher AS company, COALESCE(SUM(p.price), 0) AS sales
      FROM purchases p
      JOIN books b ON p.item_id = b.id
      WHERE p.status = 'PAID'
        AND p.item_type IN ('BOOK', 'SMARTSTORE_BOOK')
      GROUP BY b.publisher
    `);

    const templateSalesByCompany = await this.dataSource.query(`
      SELECT t.seller AS company, COALESCE(SUM(p.price), 0) AS sales
      FROM purchases p
      JOIN templates t ON p.item_id = t.id
      WHERE p.status = 'PAID'
        AND p.item_type = 'TEMPLATE'
      GROUP BY t.seller
    `);

    const totalChargePoint = await this.dataSource.query(`
      SELECT COALESCE(SUM(pp.cash_amount), 0) AS total
      FROM point_transactions pt
      JOIN point_products pp ON pp.point_amount = pt.amount
    `);

    return {
      totalMembers: +totalUsers[0].total,
      currentMembers: +currentUsers[0].total,
      deleteMembers: +deletedUsers[0].total,
      totalBooks: +totalBooks[0].total,
      totalTemplates: +totalTemplates[0].total,
      totalBookSales: +totalBookSales[0].total || 0,
      totalTemplateSales: +totalTemplateSales[0].total || 0,
      totalChargePoint: +totalChargePoint[0].total,
      bookSalesByCompany,
      templateSalesByCompany,
    };
  }
}
