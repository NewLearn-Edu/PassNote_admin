// src/app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Distributor } from './auth/distributor/distributor.entity';
import { AuthController } from './auth/auth.controller';
import { AuthService } from './auth/auth.service';
import { AuthModule } from './auth/auth.module';
import { Template } from './template/template.entity';
import { TemplateModule } from './template/template.module';
import { BookModule } from './book/book.module';
import { AdminModule } from './admin/admin.module';
import { FirebaseController } from './firebase/firebase.controller';
import { FirebaseService } from './firebase/firebase.service';
import { FirebaseModule } from './firebase/firebase.module';
import { UserModule } from './user/user.module';
import { User } from './user/user.entity';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'mysql',
      host: 'passnote-db.cx042gk4us48.ap-northeast-2.rds.amazonaws.com',
      port: 3306,
      username: 'viewer',
      password: 'viewer12!#',
      database: 'passnote',
      entities: [User, Distributor, Template],
      synchronize: false,
    }),
    UserModule,
    AuthModule,
    TemplateModule,
    BookModule,
    AdminModule,
    FirebaseModule,
  ],
})
export class AppModule {}
