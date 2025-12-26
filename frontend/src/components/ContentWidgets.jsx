import React from 'react';
import { CheckCircle2, BookOpen, Wrench, Users } from 'lucide-react';

export const SkillTree = ({ skills }) => {
    return (
        <div className="card h-full">
            <h3 className="text-xl mb-4 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-accent-sage" />
                Skill Tree
            </h3>

            <div className="space-y-6">
                <div>
                    <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Hard Skills</h4>
                    <div className="flex flex-wrap gap-2">
                        {skills.hard_skills.map((skill, i) => (
                            <span key={i} className="px-3 py-1 bg-stone-100 text-stone-700 rounded-md text-sm border border-stone-200">
                                {skill}
                            </span>
                        ))}
                    </div>
                </div>

                <div>
                    <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Tools</h4>
                    <div className="flex flex-wrap gap-2">
                        {skills.tools.map((tool, i) => (
                            <span key={i} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-md text-sm border border-blue-100">
                                {tool}
                            </span>
                        ))}
                    </div>
                </div>

                <div>
                    <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Soft Skills</h4>
                    <ul className="grid grid-cols-2 gap-2">
                        {skills.soft_skills.map((skill, i) => (
                            <li key={i} className="flex items-center gap-2 text-sm text-gray-600">
                                <span className="w-1.5 h-1.5 rounded-full bg-green-400" /> {skill}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export const StrategySection = ({ strategy }) => {
    return (
        <div className="card bg-[#FDFBF7] border-stone-200">
            <h3 className="text-xl mb-4 flex items-center gap-2">
                <Users className="w-5 h-5 text-orange-400" />
                Strategy & Advice
            </h3>
            <div className="space-y-4">
                {strategy.map((item, i) => (
                    <div key={i} className="prose">
                        <h4 className="font-serif text-lg text-gray-800 font-bold">{item.title}</h4>
                        <p className="text-gray-600 text-sm leading-relaxed">{item.content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export const ResourceList = ({ resources }) => {
    return (
        <div className="card">
            <h3 className="text-xl mb-4 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-400" />
                Curated Library
            </h3>
            <ul className="space-y-3">
                {resources.map((res, i) => (
                    <li key={i}>
                        <a
                            href={res.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 group transition-colors border border-transparent hover:border-gray-100"
                        >
                            <div>
                                <div className="font-medium text-gray-800 group-hover:text-blue-600 transition-colors">
                                    {res.name}
                                </div>
                                <div className="text-xs text-gray-500">{res.type}</div>
                            </div>
                            <span className="text-gray-300 group-hover:translate-x-1 transition-transform">→</span>
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};
