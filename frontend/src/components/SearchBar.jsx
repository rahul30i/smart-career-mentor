import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

const SearchBar = ({ onSearch, isLoading }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <div className="w-full max-w-2xl mx-auto text-center py-12">
            <div className="mb-8">
                <h1 className="text-4xl md:text-5xl mb-4 text-gray-900">Where do you want to go next?</h1>
                <p className="text-lg text-gray-600">Enter a dream role, and we'll build the map.</p>
            </div>

            <form onSubmit={handleSubmit} className="relative max-w-lg mx-auto">
                <div className="relative flex items-center">
                    <input
                        type="text"
                        className="w-full pl-6 pr-12 py-4 rounded-full border-2 border-gray-200 shadow-sm focus:border-stone-400 focus:outline-none focus:ring-2 focus:ring-stone-100 text-lg transition-all"
                        placeholder="e.g. Product Manager, AI Engineer..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        className="absolute right-2 p-2 bg-gray-900 text-white rounded-full hover:bg-gray-700 transition-colors disabled:opacity-50"
                        disabled={isLoading}
                    >
                        {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : <Search className="w-5 h-5" />}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default SearchBar;
