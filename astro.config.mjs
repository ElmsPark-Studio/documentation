// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	site: 'https://documentation.elmspark.com',
	integrations: [
		starlight({
			title: 'ElmsPark Documentation',
			description: 'Practical guides for PageMotor hosting and EP Suite plugins.',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/ElmsPark-Studio/documentation' },
			],
			customCss: [
				'./src/styles/custom.css',
			],
			editLink: {
				baseUrl: 'https://github.com/ElmsPark-Studio/documentation/edit/main/',
			},
			head: [
				{
					tag: 'link',
					attrs: { rel: 'preconnect', href: 'https://fonts.bunny.net', crossorigin: true },
				},
				{
					tag: 'link',
					attrs: {
						rel: 'stylesheet',
						href: 'https://fonts.bunny.net/css?family=fraunces:600,700|outfit:300,400,500,600|jetbrains-mono:400&display=swap',
					},
				},
			],
			sidebar: [
				{
					label: 'Start here',
					items: [
						{ label: 'Welcome', slug: 'index' },
					],
				},
				{
					label: 'Hosting',
					items: [
						{ label: 'Vultr for PageMotor', slug: 'hosting/vultr' },
					],
				},
				{
					label: 'EP Suite plugins',
					autogenerate: { directory: 'plugins' },
				},
			],
			lastUpdated: true,
			pagination: true,
		}),
	],
});
