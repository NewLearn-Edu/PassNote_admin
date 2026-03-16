import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import * as bcrypt from 'bcrypt';
import { Distributor } from './distributor/distributor.entity';
import { LoginDto } from './dto/login.dto';

@Injectable()
export class AuthService {
  constructor(
    private jwtService: JwtService,
    @InjectRepository(Distributor)
    private distributorRepository: Repository<Distributor>,
  ) {}

  async validateUser(email: string, password: string): Promise<any> {
    const result = await this.distributorRepository.query(
      `
        SELECT
          cm.id AS distributor_id,
          cm.email,
          cm.name,
          c.name AS company,
          cm.password,
          cm.role AS type
        FROM company_managers cm
        JOIN companies c
          ON cm.company_id = c.id
        WHERE cm.email = ?
      `,
      [email],
    );

    const user = result[0];
    if (user && (await bcrypt.compare(password, user.password))) {
      return user;
    }
    throw new UnauthorizedException('이메일 또는 비밀번호가 잘못되었습니다');
  }

  async login(user: any) {
    const payload = {
      sub: user.distributor_id,
      email: user.email,
      name: user.name,
      company: user.company,
      type: typeof user.type === 'string' ? user.type.toLowerCase() : user.type,
    };
    return this.jwtService.sign(payload);
  }
}
