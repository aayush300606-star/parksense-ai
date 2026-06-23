class TrafficSpeedEngine:
    """
    Calculates the degraded current speed of traffic due to illegal parking
    using a calibrated adaptation of the Bureau of Public Roads (BPR) function.
    
    BPR Function (standard form):
        t = t0 * [1 + α * (V/C)^β]
    
    Our adaptation reinterprets (V/C) as effective capacity loss:
        When parking reduces effective road width, it reduces capacity C.
        If demand V stays constant but C shrinks, the V/C ratio rises,
        causing speed to drop.
    
    We model:
        Adjusted V/C = Base V/C + (Capacity Loss % / 100) * Amplification Factor
        Speed Factor = 1 / [1 + α * (Adjusted V/C)^β]
        Current Speed = Base Speed * Speed Factor
    
    Calibration parameters α=0.15, β=4.0 follow the standard BPR function
    with α tuned down from the highway default of 0.15 since we're in urban context.
    """

    # BPR calibration constants
    ALPHA = 0.15    # Sensitivity coefficient
    BETA = 4.0      # Exponential growth factor (standard BPR uses 4)
    
    # How much a 1% capacity loss amplifies the V/C ratio
    # Higher values = more aggressive speed drops for same capacity loss
    CAPACITY_LOSS_AMPLIFIER = 1.2

    @staticmethod
    def calculate_current_speed(
        base_speed_kmh: float,
        base_vc_ratio: float,
        capacity_loss_percentage: float
    ) -> dict:
        """
        Computes the degraded speed using the BPR-adapted model.
        
        Args:
            base_speed_kmh: Free-flow speed (km/h)
            base_vc_ratio: Baseline volume/capacity ratio under free-flow
            capacity_loss_percentage: How much capacity is lost due to parking (0-100)
            
        Returns:
            dict with:
                - current_speed_kmh: Degraded speed
                - speed_reduction_kmh: Absolute reduction
                - speed_reduction_percentage: Relative reduction (0-100)
                - speed_reduction_severity: Categorical severity
                - adjusted_vc_ratio: The effective V/C after parking impact
                - model_used: Attribution
        """
        # Clamp capacity loss to physical bounds
        cap_loss = max(0.0, min(100.0, capacity_loss_percentage))
        
        # Calculate adjusted V/C ratio
        # As parking eats capacity, V/C rises proportionally
        vc_increase = (cap_loss / 100.0) * TrafficSpeedEngine.CAPACITY_LOSS_AMPLIFIER
        adjusted_vc = base_vc_ratio + vc_increase
        
        # BPR speed degradation
        # Speed Factor = 1 / [1 + α * (V/C)^β]
        bpr_denominator = 1 + TrafficSpeedEngine.ALPHA * (adjusted_vc ** TrafficSpeedEngine.BETA)
        speed_factor = 1.0 / bpr_denominator
        
        current_speed = base_speed_kmh * speed_factor
        
        # Enforce minimum crawl speed (vehicles never truly stop in flow model)
        current_speed = max(current_speed, 3.0)
        
        speed_reduction = base_speed_kmh - current_speed
        
        if base_speed_kmh > 0:
            reduction_pct = (speed_reduction / base_speed_kmh) * 100.0
        else:
            reduction_pct = 0.0
        
        # Severity classification
        if reduction_pct >= 60:
            severity = "Critical"
        elif reduction_pct >= 40:
            severity = "Severe"
        elif reduction_pct >= 25:
            severity = "Moderate"
        elif reduction_pct >= 10:
            severity = "Low"
        else:
            severity = "Minimal"
        
        return {
            "current_speed_kmh": round(current_speed, 2),
            "speed_reduction_kmh": round(speed_reduction, 2),
            "speed_reduction_percentage": round(reduction_pct, 2),
            "speed_reduction_severity": severity,
            "adjusted_vc_ratio": round(adjusted_vc, 4),
            "model_used": "BPR-Adapted Urban Model (α=0.15, β=4.0)"
        }
