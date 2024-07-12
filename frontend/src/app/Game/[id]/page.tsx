'use client';

import "./page.css";
import { useEffect, useRef, useState } from "react";
import axios from 'axios';
import Referee from '../../components/Referee/Referee';
import { useParams } from 'next/navigation'

export default function Game() {
    const searchParams = useParams<{ id: string }>()
    let id: number = parseInt(searchParams.id);
    return (
        <main id="app" className="p-24">
            <Referee id={id}/>
        </main>
    );
}