import React, { useState } from 'react';
import axios from 'axios';

const LexerTester: React.FC = () => {
    const [code, setCode] = useState(`# Load genomic data
LOAD FASTA "reference.fa" -> genome
LOAD VCF "variants.vcf" -> variants

# Analyze sequences
ANALYZE genome COUNT_GC -> gc_content`);
    
    const [tokens, setTokens] = useState<any[]>([]);
    const [error, setError] = useState<string>('');

    const analyzeCode = async () => {
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_URL}/analyze`, { code });
            setTokens(response.data.tokens);
            setError('');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'An error occurred');
            setTokens([]);
        }
    };

    return (
        <div className="lexer-tester">
            <h2>GenomeScript Lexer Tester</h2>
            <div className="editor-container">
                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    rows={10}
                    placeholder="Enter GenomeScript code..."
                />
                <button onClick={analyzeCode}>Analyze</button>
            </div>
            
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}
            
            {tokens.length > 0 && (
                <div className="tokens-container">
                    <h3>Tokens:</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Line</th>
                                <th>Column</th>
                                <th>Type</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tokens.map((token, index) => (
                                <tr key={index}>
                                    <td>{token.line}</td>
                                    <td>{token.column}</td>
                                    <td>{token.type}</td>
                                    <td>{token.value}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default LexerTester; 