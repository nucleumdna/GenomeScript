import React from 'react';

interface GenomeScriptEditorProps {
    value: string;
    onChange: (value: string) => void;
}

export const GenomeScriptEditor: React.FC<GenomeScriptEditorProps> = ({ value, onChange }) => {
    return (
        <div>
            <textarea 
                value={value} 
                onChange={(e) => onChange(e.target.value)}
                style={{ width: '100%', height: '400px' }}
            />
        </div>
    );
}; 