module.exports = function (grunt) {
  require('jit-grunt')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    less: {
      build: {
        options: {
          plugins: [
            new (require('less-plugin-autoprefix'))({ browsers: ['> 2%'] })
          ],
          compress: true
        },
        files: {
          'django_learnit/static/django_learnit/css/style.min.css': 'styles/style.less'
        }
      }
    },

    watch: {
      options: {
        spawn: false
      },
      styles: {
        files: ['styles/**/*.less'],
        tasks: ['less:build']
      }
    }
  });
};
