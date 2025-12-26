import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

const Roadmap = ({ chart }) => {
    const containerRef = useRef(null);

    useEffect(() => {
        mermaid.initialize({
            startOnLoad: true,
            look: 'hand', // Experimental hand-drawn look
            theme: 'base',
            themeVariables: {
                primaryColor: '#fef3c7', // amber-100
                primaryTextColor: '#451a03',
                primaryBorderColor: '#78350f',
                lineColor: '#78350f',
                secondaryColor: '#bfdbfe',
                tertiaryColor: '#fff',
                fontFamily: 'Merriweather', // Switch to serif for that academic/human feel
            },
            flowchart: {
                curve: 'basis', // Smooth curves
                htmlLabels: true,
            },
            securityLevel: 'loose',
        });

        const renderChart = async () => {
            if (containerRef.current && chart) {
                containerRef.current.innerHTML = ''; // Start clean
                try {
                    const { svg } = await mermaid.render('mermaid-chart-' + Date.now(), chart);
                    containerRef.current.innerHTML = svg;
                } catch (err) {
                    console.error('Mermaid render error:', err);
                    containerRef.current.innerHTML = '<p class="text-red-500">Failed to render roadmap</p>';
                }
            }
        };

        renderChart();
    }, [chart]);

    return (
        <div className="card h-full min-h-[400px] flex flex-col">
            <h3 className="text-lg mb-4 text-gray-700 border-b border-gray-100 pb-2">Visual Roadmap</h3>
            <div
                ref={containerRef}
                className="flex-grow flex items-center justify-center overflow-auto p-4"
                style={{ minHeight: '300px' }}
            />
        </div>
    );
};

export default Roadmap;
