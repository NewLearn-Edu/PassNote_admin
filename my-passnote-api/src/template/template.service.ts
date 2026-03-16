import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Template } from './template.entity';

@Injectable()
export class TemplateService {
  constructor(
    @InjectRepository(Template)
    private templateRepository: Repository<Template>,
  ) {}

  async findBySeller(company: string): Promise<Template[]> {
    return this.templateRepository.find({ where: { seller: company } });
  }

  async findPurchasesBySeller(company: string) {
    const raw = await this.templateRepository.query(`
      SELECT
        t.name AS templateName,
        tp.price,
        tp.created_at,
        tp.is_refunded
      FROM template t
      JOIN template_purchase tp ON t.template_id = tp.template_id
      JOIN users u ON tp.member_id = u.id
      WHERE t.seller = ?
    `, [company]);

    return raw.map((row) => ({
        ...row,
        created_at: new Date(row.created_at).toISOString().replace('T', ' ').split('.')[0] // ✅ 타임존 제거
      }));
  }
}
