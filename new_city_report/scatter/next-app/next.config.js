/** @type {import('next').NextConfig} */

const report = process.env.REPORT;

const nextConfig = !report
  ? {
      output: "export",
      distDir: "out",
    }
  : {
      output: "export",
      distDir: `../pipeline/outputs/${report}/report`,
      assetPrefix: "./",
      env: { REPORT: report },
      server: {
        host: '0.0.0.0'
      }
    };

module.exports = nextConfig;
