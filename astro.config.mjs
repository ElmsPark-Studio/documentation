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
