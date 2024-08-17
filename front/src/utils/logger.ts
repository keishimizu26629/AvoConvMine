import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    // コンソールにログを出力
    new winston.transports.Console(),
    // サーバーサイドのみでファイルにログを出力
    ...(process.browser ? [] : [new winston.transports.File({ filename: 'combined.log' })])
  ],
});

export default logger;
