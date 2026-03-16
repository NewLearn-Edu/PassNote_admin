import { Controller, Get, UseGuards, Request } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { BookService } from './book.service';

@Controller('books')
export class BookController {
  constructor(private readonly bookService: BookService) {}

  @UseGuards(JwtAuthGuard)
  @Get('company')
  async getBooksByCompany(@Request() req) {
    const companyName = req.user.company;
    return this.bookService.findBooksByCompany(companyName);
  }

  @UseGuards(JwtAuthGuard)
  @Get('purchases')
  async getPurchases(@Request() req) {
    const company = req.user.company;
    return this.bookService.findPurchasesByCompany(company);
  }
}