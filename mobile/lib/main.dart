import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import 'presentation/app.dart';
final dioProvider = Provider<Dio>((ref) => Dio(BaseOptions(baseUrl: 'http://localhost:8000')));

void main() {
  runApp(
    const ProviderScope(
      child: App(),
    ),
  );
}
