import { Module } from '@nestjs/common';
import { AdminController } from './admin.controller';
import { AdminService } from './admin.service';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [TypeOrmModule.forFeature([])], // 이미 app.module에서 설정된 경우 생략 가능
  controllers: [AdminController],
  providers: [AdminService],
})
export class AdminModule {}