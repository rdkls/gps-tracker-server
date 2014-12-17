var gulp = require('gulp'),
    sass = require('gulp-sass'),
    jade = require('gulp-jade');

gulp.task('default', ['jade', 'jade_index', 'sass']);

gulp.task('sass', function(){
  return gulp.src('styles/main.scss')
    .pipe(sass({ style: 'compressed' }))
    .pipe(gulp.dest('styles'));
});

gulp.task('jade_index', function(){
  return gulp.src('*.jade')
    .pipe(jade({ pretty: true }))
    .pipe(gulp.dest('.'));
});

gulp.task('jade', function(){
  return gulp.src('views/**/*.jade')
    .pipe(jade({ pretty: true }))
    .pipe(gulp.dest('views'));
});

gulp.task('watch', ['jade', 'jade_index', 'sass'], function(){
  gulp.watch('styles/*.scss', ['sass']);
  gulp.watch('views/*.jade', ['jade']);
  gulp.watch('*.jade', ['jade_index']);
});
