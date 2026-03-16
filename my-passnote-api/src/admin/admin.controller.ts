import { Controller, Get, UseGuards, Request, Logger } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { AdminService } from './admin.service';

@Controller('admin')
export class AdminController {
  constructor(private readonly adminService: AdminService) {}

  @UseGuards(JwtAuthGuard)
  @Get('statistics')
  getStatistics(@Request() req) {
    return this.adminService.getStatistics(req.user);
  }
}