import { Controller, Post, Body, Res, HttpCode } from '@nestjs/common';
import { Response } from 'express';
import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';

@Controller('distributor')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('login')
  @HttpCode(200)
  async login(@Res({ passthrough: true }) res: Response, @Body() loginDto: LoginDto) {
    const distributor = await this.authService.validateUser(loginDto.email, loginDto.password);
    const token = await this.authService.login(distributor);
  
    res.cookie('distributorToken', token, {
      httpOnly: false,
      secure: false,
      maxAge: 3600 * 1000,
      sameSite: 'lax',
    });
  
    return { message: '로그인 성공', type: distributor.type, name: distributor.name};
  }
}