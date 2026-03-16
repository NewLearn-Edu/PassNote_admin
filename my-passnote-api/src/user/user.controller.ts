// src/user/user.controller.ts
import { Controller, Get } from '@nestjs/common';
import { UserService } from './user.service';
import { User } from './user.entity';

@Controller('members')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  async findAll() {
    const users = await this.userService.findAll();

    return users.map((user) => ({
      memberId: user.userId,
      email: user.email,
      name: user.name,
      nickname: user.nickname,
      target_career: user.target_career,
      animal_image: user.animalType,
      point: user.point,
      created_at: user.created_at,
    }));
  }
}
