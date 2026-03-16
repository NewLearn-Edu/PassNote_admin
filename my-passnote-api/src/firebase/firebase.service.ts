import { Injectable, OnModuleInit } from '@nestjs/common';
import * as admin from 'firebase-admin';
const koreanhistory = require('./koreanhistory.json');
const koreanhistoryexam = require('./koreanhistoryexam.json');
const passnote = require('./passnote.json');
const policescience = require('./policescience.json');

@Injectable()
export class FirebaseService implements OnModuleInit {
  onModuleInit() {
    admin.initializeApp({ credential: admin.credential.cert(passnote) }, 'passnote');
    admin.initializeApp({ credential: admin.credential.cert(koreanhistory) }, 'koreanhistory');
    admin.initializeApp({ credential: admin.credential.cert(koreanhistoryexam) }, 'koreanhistoryexam');
    admin.initializeApp({ credential: admin.credential.cert(policescience) }, 'policescience');
  }

  async sendToTopic(appName: string, topic: string, title: string, body: string) {
    const message = { notification: { title, body }, topic };
    return admin.app(appName).messaging().send(message);
  }
}