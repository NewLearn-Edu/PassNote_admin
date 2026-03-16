import { Controller, Post, Body } from '@nestjs/common';
import { FirebaseService } from './firebase.service';

@Controller('notification')
export class FirebaseController {
  constructor(private readonly firebaseService: FirebaseService) {}

  @Post('send/koreanhistory')
  sendKoreanHistory(@Body() body: { title: string; message: string }) {
    return this.firebaseService.sendToTopic('koreanhistory', 'all', body.title, body.message);
  }

  @Post('send/koreanhistoryexam')
  sendKoreanHistoryExam(@Body() body: { title: string; message: string }) {
    return this.firebaseService.sendToTopic('koreanhistoryexam', 'all', body.title, body.message);
  }

  @Post('send/policescience')
  sendPoliceScience(@Body() body: { title: string; message: string }) {
    return this.firebaseService.sendToTopic('policescience', 'all', body.title, body.message);
  }

  @Post('send/passnote')
  sendPassnote(@Body() body: { title: string; message: string }) {
    return this.firebaseService.sendToTopic('passnote', 'all', body.title, body.message);
  }
}