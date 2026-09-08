// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

// URL path fragments excluded from the public sitemap.
// Pages in this list stay live at their URL but are not advertised
// to crawlers via sitemap.xml. Pair with `sidebar.hidden`,
// `pagefind: false` and a robots noindex meta tag in frontmatter.
const UNLISTED_URL_FRAGMENTS = [
	'pm-managed-server-hosts',
];

export default defineConfig({
	site: 'https://documentation.elmspark.com',
	integrations: [
		sitemap({
			filter: (page) => !UNLISTED_URL_FRAGMENTS.some((frag) => page.includes(frag)),
		}),
		starlight({
			title: 'EP Suite Documentation',
			description: 'User guides for every EP Suite plugin. Setup, configuration, troubleshooting, real-world examples.',
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
					label: 'EP Suite plugins',
					autogenerate: { directory: 'plugins' },
				},
				{
					label: 'Hosting',
					items: [
						{ label: 'Vultr for PageMotor', slug: 'hosting/vultr' },
					],
				},
			],
			lastUpdated: true,
			pagination: true,
		}),
	],
});
