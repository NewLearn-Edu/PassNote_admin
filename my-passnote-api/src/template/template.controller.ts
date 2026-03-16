import { Controller, Get, UseGuards, Request, Logger } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { TemplateService } from './template.service';

@Controller('template')
export class TemplateController {
  constructor(private readonly templateService: TemplateService) {}

  @UseGuards(JwtAuthGuard)
  @Get('company')
  async getTemplatesByCompany(@Request() req) {
    const company = req.user.company;
    return this.templateService.findBySeller(company);
  }

  @UseGuards(JwtAuthGuard)
  @Get('purchases')
  async getPurchases(@Request() req) {
    const company = req.user.company;
    return this.templateService.findPurchasesBySeller(company);
  }
}