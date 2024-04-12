import HomeIcon from './icons/HomeIcon.svelte';
import StatusIcon from './icons/StatusIcon.svelte';
import ArchivesIcon from './icons/ArchivesIcon.svelte';
import SettingsIcon from './icons/SettingsIcon.svelte';
import DocumentationIcon from './icons/DocumentationIcon.svelte';

export const data = [
	{
		title: 'Home',
		icon: HomeIcon,
		link: '/'
	},
	{
		title: 'Projects',
		icon: StatusIcon,
		link: '/admin/projects'
	},
	{
		title: 'Agents',
		icon: ArchivesIcon,
		link: '/admin/agents'
	},
	{
		title: 'Settings',
		icon: SettingsIcon,
		link: '/admin/settings'
	},
	{
		title: 'Documentation',
		icon: DocumentationIcon,
		link: '/admin/documentation'
	}
];
