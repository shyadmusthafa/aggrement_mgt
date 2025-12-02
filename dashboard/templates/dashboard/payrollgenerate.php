<?php


	/*Payroll generate Start */
	function payrollgenerate($MonthAndYear,$company1,$Company_id,$CompanyGroup_id,$PrivilegeUserName,$request)
	{
		$auser=DotC::getUser($request->header('Authorization'));
		$user=HrmProfile::where('id', $auser->sub)->first();

		$json_arry=array();
		$Error=array();

		$lophour=0;
		$SNo=0;
					
		if($filter)
		$filter=" and u_name='".strtoupper($filter)."'  ";
		$MonthAndYear=$this->PayGenerateLive($CompanyGroup_id);
		

		$getPayGrpName=DB::select("SELECT * FROM hrm_payroll_group a WHERE a.id='".$CompanyGroup_id."' ");
		$tax_calc=$getPayGrpName[0]->incometax_calculation;

		if($Company_id)
		{
			if($MonthAndYear)
			{					
				$this->PaygenerateDelete($MonthAndYear, $CompanyGroup_id, $filter );

				$PrivilegeName='1679091c5a880faf6fb5e6087eb1b2dc';

				DB::getPdo()->setAttribute(PDOConnection::ATTR_EMULATE_PREPARES, true);

				$s0=DB::select('CALL payscale_data_generate(?, ?,?,?)', [$PrivilegeUserName,$PrivilegeName,$CompanyGroup_id,$MonthAndYear]);
				$s0 = array_map(function ($value) {
					return (array)$value;
				}, $s0);

				$FromMonthAndYear=date('Y-m-01', strtotime($MonthAndYear));
				$ToMonthAndYear=date('Y-m-t', strtotime($MonthAndYear));
				$Notification=array();

				foreach ($s0 as $key => $value) 
				{
					if($value['DOR']>=$FromMonthAndYear && $value['DOR']<=$ToMonthAndYear)
					{
						if($value['extension_date']=='')
							$Notification[]['notification']=$value['u_name'].": Retirement Date : ".date('d-m-Y',strtotime($value['DOR']))." With No Extension";
						else
							$Notification[]['notification']=$value['u_name'].": Retirement Date : ".date('d-m-Y',strtotime($value['DOR']))." Extension Date:".$value['extension_date'];
					}

					if($value['last_working_date']>=$FromMonthAndYear && $value['last_working_date']<=$ToMonthAndYear)
					{
						if($value['preActive']=='2')
							$Notification[]['notification']=$value['u_name'].": Last Working Date : ".date('d-m-Y',strtotime($value['DOR']))." With Hold Salary";
						else
							$Notification[]['notification']=$value['u_name'].": Last Working Date : ".date('d-m-Y',strtotime($value['last_working_date']))." Without Hold Salary";
					}
				}

				/*incometax start*/
				if($MonthAndYear > '2024-01' && $tax_calc=='Auto'){
					$payscaleStaffProfile1=array();
					$r=$s0;
					for($i=0;$i<count($r);$i++){
						$payscaleStaffProfile1[$r[$i]['u_name']]=$r[$i];
					}

					
					foreach($payscaleStaffProfile1 as $key5 => $value5)
					{
						$req=new Request();
						$Fin_year = HrmPayrollGroupController::getFinYear ($req);
						$finYear=$Fin_year['finyear'];
						$get_type=DB::select("SELECT * FROM hrm_payroll_incometax_submission a 
												WHERE a.u_name='".$key5."' AND a.fin_year='".$finYear."' AND a.`status`=1 GROUP BY a.u_name,a.`type`");
						$get_type=json_decode(json_encode($get_type), true);
			
						$get_ctc=DB::select(" SELECT * FROM mas_ctc a WHERE a.emp_code='".$key5."' ORDER BY id DESC LIMIT 1 ");
						$get_ctc=json_decode(json_encode($get_ctc), true);
						$get_ctc_id=$get_ctc['0']['id'];
			
						if(!empty($get_ctc_id)){
							$request=new request();
							$request->company_name=$CompanyGroup_id;
							$request->FinishedFilter=1;
							$request->option=1;
							$request->user_name=$key5;
							$request->fin_yr=$finYear;
							$request->mode='Form_2';
							$request->deduction_method='config';
			
							if(!empty($get_type)){
								$request->type=$get_type['0']['type'];
							}else{
								$request->type='new';
							}
			                $final_data="";
							$getEmpDatas=DB::select("SELECT company_id,location_id,payroll_group_id FROM profile a WHERE a.emp_code='".$key5."' ");
			
							$tax_data=HrmIncomeTaxController::IncomeTaxCalculationSheet($request);
							$data1=json_encode($tax_data,true);
							$data=json_decode($data1,true);
							
							$final_data=$data['original']['result'][0];
							$heading = $final_data['heading'];
							$total_earning_txt = 'Total Earnings';

							$save_pdf="";
							$save_pdf .="<html>
							<head>
							<style>
								.card-header {
								border: 1px solid #8bc34a;
								}
								.card-body {
									flex: 1 1 auto;
									padding: 1.25rem;
								}
								.mat-dialog-title {
									margin: 0 0 20px;
									display: block;
									font-size: 16px;
									letter-spacing: .5px;
									font-weight: 700;
									margin-bottom: 8px!important;
									text-transform: uppercase;
								}
								.mat-dialog-content {
									display: block;
									margin: 0 -24px;
									padding: 0 24px;
								}
								.small, small {
									font-size: 80%;
									font-weight: 400;
								}
								.text-align-left {
									text-align:left;
								}
								.table {
								border-collapse: collapse;
								}
								.border1 {
									border:1px solid #ccc !important;
								}
								.table thead {
									background: #6c757dd1;
								}
								.table {
									width: 100%;
									margin-bottom: 1rem;
									background-color: #fff;
								}	
								.table-bordered {
									border: 1px solid #e9ecef;
								}
								.width-adjusted {
									width: 100%;
								}
								.table thead th {
									color: #fff;
									font-weight: 400;
									letter-spacing: .8px;
									text-transform: uppercase;
								}
								.table-bordered, .table-bordered td, .table-bordered th {
									border: 1px solid #e9ecef;
								}
							</style>
							</head>
							<body>
								<div class='row' style='text-align:center;border: 1px solid #8bc34a'>
									<div class='card-header mat-dialog-title' >COMPUTATION SHEET FOR THE FINANCIAL YEAR:".$final_data['heading']['fin_year']."</h2>
								</div>
								<div class='card-body'>
								<div class='mat-dialog-content'>
									<table class='table table-bordered' id='computation_data'>
									<div class='row' style='width: 100%;'>
										<table class='table table-bordered' style='border:1px solid #ccc !important;width:100%;'>
											<tbody>
												<tr class='active border1'>
													<td class='text-align-left border1' colspan='2' >
														<span class='big'><b>".$heading['Company']."</b></span><br>"
														.$heading['location']."<br>"
														.$heading['company_group']."<br><br>
														<span class='small'>".$heading['head_line']."</span>
													</td>
													<td class='border1' colspan='2'></td>
												</tr>";
												foreach ($final_data['head1'] as $i => $res){
													$save_pdf.="<tr>
																	<td class='text-align-left border1' colspan='2'>".$res['head']."</td>
																	<td class='text-align-left border1' colspan='2'>".$final_data['data1'][$i]['data']."</td>
																</tr>";
												}
												$save_pdf.="</tbody>
										</table> 
								
										<table class='table table-bordered width-adjusted' align='center'>
											<thead>
												<tr>";
												foreach($final_data['head'] as $j=> $res1){
													if($res1['line']=='1'){
														$save_pdf.="<th rowspan='".$res1['rowspan']."' colspan='".$res1['colspan']."'><span>".$res1['label']."</span></th>";
													}
												}
												$save_pdf.="</tr>
											</thead>
											<tbody>";
												foreach($final_data['earning'] as $k=> $res2){
													$save_pdf.="<tr>
														<td style='text-align: left;'>".$res2['Name']."</td>
														<td style='text-align: right;'>".$res2['PaidAmount']."</td>
														<td style='text-align: right;'>".$res2['CurrentMonthAmount']."</td>
														<td style='text-align: right;'>".$res2['RemainingAmount']."</td>
														<td style='text-align: right;'>".$res2['total']."</td>
													</tr>";
												}		
											$save_pdf.= "</tbody>
											<tfoot>
											<tr>
												<td style='text-align: left;'><b>".$total_earning_txt."</b></td>
												<td style='text-align:right;'><b>".$final_data['earning_paid']['total_paid_earning']."</b></td>
												<td style='text-align:right;'><b>".$final_data['earning_actual_cur_month']['total_actual_earning_cur_month']."</b></td>
												<td style='text-align:right;'><b>".$final_data['earning_actual']['total_actual_earning']."</b></td>
												<td style='text-align:right;'><b>".number_format(($final_data['earning_paid']['total_paid_earning']+$final_data['earning_actual_cur_month']['total_actual_earning_cur_month']+$final_data['earning_actual']['total_actual_earning']),2)."</b></td>
											</tr>
											</tfoot>	
										</table> 
			
										<table class='table table-bordered width-adjusted' align='center'>";
											if($final_data && $final_data['data3']) {
												foreach($final_data['data3'] as $m=> $res3){
													$save_pdf.="<tbody>
													<tr>
														<td colspan='3' style='text-align: left;'>".$res3['label']."</td>
														<td colspan='1' style='text-align: right;'>".$res3['value2']."</td>
													</tr>";
												}
			
												$save_pdf.="</tbody>
														<tfoot>
														<tr>
															<td colspan='3' style='text-align: left;'><b>Total Deduction</b></td>
															<td colspan='1' style='text-align: right'><b>".number_format($final_data['deduction_total']['deduction_total'],2)."</b></td>
														</tr>
														</tfoot>";
											}
												
										$save_pdf.="</table>
			
										<table class='table table-bordered width-adjusted' align='center'>";
											if($final_data && $final_data['rental_declaration']) {
												$save_pdf.="<thead>
																<tr>
																	<th style='text-align: left;' colspan='3' >Rental Declaration</th>
																	<th style='text-align: left;' colspan='1' >Amount</th>
																</tr>
															</thead>";
												foreach($final_data['rental_declaration'] as $n=> $res4){
													$save_pdf.="<tbody>
																	<tr>
																		<td colspan='3' style='text-align: left;'>".$res4['section']."</td>
																		<td colspan='1' style='text-align: right;'>".$res4['amount']."</td>
																</tr>";
												}
												$save_pdf.="</tbody>
														<tfoot >";
														if($final_data['total_rental_declaration']['total_rental_declaration1'] !=null){
												$save_pdf.="<tr>
																<td colspan='3' style='text-align: left;'><b>Total&nbsp;Rental&nbsp;Income</b></td>
																<td colspan='1' style='text-align: right;'><b>".number_format($final_data['total_rental_declaration']['total_rental_declaration1'],2)."</b></td>
															</tr>";
															}
															if($final_data['total_rental_savings']['total_rental_savings'] !=null){
												$save_pdf.="<tr>
																<td colspan='3' style='text-align: left;'><b>Total&nbsp;Rental&nbsp;Savings</b></td>
																<td colspan='1' style='text-align: right;''><b>".number_format($final_data['total_rental_savings']['total_rental_savings'],2)."</b></td>
															</tr>";
															}
												$save_pdf.="</tfoot>";
											}
											
										$save_pdf.="</table>
			
										<table class='table table-bordered width-adjusted' align='center'>";
											if($final_data && $final_data['other_decalaration']) {
												foreach($final_data['other_decalaration'] as $o=> $res5){
													$save_pdf.="<tbody>
													<tr>
														<td colspan='3' style='text-align: left;'>".$res5['section']."</td>
														<td colspan='1' style='text-align: right;'>".$res5['amount']."</td>
													</tr>";
												}
			
												$save_pdf.="</tbody>
														<tfoot>
														<tr>
															<td colspan='3' style='text-align: left;'><b>Total Other Income</b></td>
															<td colspan='1' style='text-align: right'><b>".number_format($final_data['total_other_declaration']['total_other_declaration'],2)."</b></td>
														</tr>
														</tfoot>";
											}
										$save_pdf.="</table>
			
										<table class='table table-bordered width-adjusted' align='center'>";
											if($final_data && $final_data['declaration']) {
												$save_pdf.="<thead>
																<tr>
																	<th style='text-align: left;' colspan='3' >Less: Deductions under Chapter VI-A</th>
																	<th style='text-align: left;' colspan='1' >Amount</th>
																</tr>
												</thead>";
												foreach($final_data['declaration'] as $p=> $res6){
													$save_pdf.="<tbody>
													<tr>
														<td colspan='3' style='text-align: left;'>".$res6['section']."</td>
														<td colspan='1' style='text-align: right;'>".$res6['amount']."</td>
													</tr>";
												}
			
												$save_pdf.="</tbody>
														<tfoot>
														<tr>
															<td colspan='3' style='text-align: left;'><b>Total&nbsp;Less:&nbsp;Deductions&nbsp;under&nbsp;Chapter&nbsp;VI-A</b></td>
															<td colspan='1' style='text-align: right'><b>".number_format($final_data['total_declaration_amount']['total_declaration'],2)."</b></td>
														</tr>
														</tfoot>";
											}
										$save_pdf.="</table>
			
										<table class='table table-bordered width-adjusted' >
											<tbody>";
												foreach($final_data['data2'] as $q=> $res7){
													$save_pdf.="<tr>";
																	if($res7['label']){
																		$save_pdf.="<td style='text-align:".$res7['td_align'].";color:".$res7['label_color'].";background:".$res7['td_color']." ' colspan=".$res7['label_colspan']." >";
																		if($res7['label3_color']){
																			$save_pdf.="<span><b>".$res7['label']."</b></span>";
																		}
			
																		if(!$res7['label3_color']){
																			$save_pdf.="<span>".$res7['label']."</span>";
																		}
																		$save_pdf.="</td>";
																	}
			
																	if($res7['value1']){
																		$save_pdf.="<td style='text-align: right' colspan=".$res7['value1_colspan'].">";
																		if($res7['value1_color']){
																			$save_pdf.="<span><b>".$res7['value1']."</b></span>";
																		}
			
																		if(!$res7['value1_color']){
																			$save_pdf.="<span><b>".$res7['value1']."</b></span>";
																		}		
																		$save_pdf.="</td>";
																	}
			
																	if($res7['value4']){
																		$save_pdf.="<td style='text-align: right' colspan=".$res7['colspan']." >".$res7['value4']."</td>";
																	}
			
																	if($res7['value2']){
																		$save_pdf.="<td style='text-align: right' colspan=".$res7['value2_colspan'].">";
																		if($res7['value2_color']){
																			$save_pdf.="<span><b>".$res7['value2']."</b></span>";
																		}
			
																		if(!$res7['value2_color']){
																			$save_pdf.="<span><b>".$res7['value2']."</b></span>";
																		}		
																		$save_pdf.="</td>";
																	}
			
																	if($res7['value3']){
																		$save_pdf.="<td style='text-align: right' colspan=".$res7['value3_colspan'].">";
																		if($res7['value3_color']){
																			$save_pdf.="<span><b>".$res7['value3']."</b></span>";
																		}
			
																		if(!$res7['value3_color']){
																			$save_pdf.="<span><b>".$res7['value3']."</b></span>";
																		}		
																		$save_pdf.="</td>";
																	}
			
																	$save_pdf.="</tr>";
												}
										$save_pdf.="</tbody></table>
			
									</div> 
									</table>
								</div>
								</div>
							</body></html>";
						
							

							$pdfPath ='Month_Wise_Incometax_Save/Incometax_sheet_'.$MonthAndYear.'_'.$key5.'.pdf'; 
							//$pdfPath->move(DotC::public_path('Month_Wise_Incometax_Save/Incometax_sheet_'.$MonthAndYear.'_'.$key5.'.pdf '));
							$file_name='Month_Wise_Incometax_Save/Incometax_sheet_'.$MonthAndYear.'_'.$key5.'.pdf';  
							$pdf = Facade::loadHTML($save_pdf)->setPaper('a3', 'portrait');
							$pdf->save($pdfPath);

							$tot_earnings=" ";
							$tot_earnings=($final_data['earning_actual']['total_actual_earning']+$final_data['earning_actual_cur_month']['total_actual_earning_cur_month']+$final_data['earning_paid']['total_paid_earning']);
							$getExistingData=DB::select("SELECT * FROM hrm_payscale a WHERE u_name='".$key5."' AND data_name='D008' AND `From`='".$MonthAndYear."' AND `To`='".$MonthAndYear."' ");
			
							$request1->company_name=$CompanyGroup_id;
							$request1->FinishedFilter=1;
							$request1->option=1;
							$request1->user_name=$key5;
							$request1->data='IT_deduction';
							$request1->fin_yr=$finYear;
							$request1->mode='Form_2';
							$request1->deduction_method='config';
			
							if(!empty($get_type)){
							 	$request1->type=$get_type['0']['type'];
							}else{
								$request1->type='new';
							}
				
							// $reqq=new Request();
							// $jsonData="";
							// $it_array=HrmIncomeTaxController::IncomeTaxCalculationSheet($reqq,$request1);
							// $decoded_json =json_encode($it_array, true);
							// $jsonData = json_decode($decoded_json,true);

							//return $jsonData ;

							// $tax_data=HrmIncomeTaxController::IncomeTaxCalculationSheet($request);
							// $data1=json_encode($tax_data,true);
							// $data=json_decode($data1,true);

							$checkManualIT=DB::select("SELECT * FROM hrm_payroll_monpayr_incometax_manual a WHERE a.emp_code='".$key5."' and a.monthandyear='".$MonthAndYear."' ");

							$cur_month="";
							$cur_month=intval(str_replace( ',', '',$final_data['current_month_it']));

							if(empty($checkManualIT)){ 
								$delete_payscale=DB::delete("DELETE FROM hrm_payscale WHERE u_name='".$key5."' AND `from`='".$MonthAndYear."' and `to`='".$MonthAndYear."' AND data_name='D008'  ");
							}
							// if(empty($getExistingData)){
								if($cur_month>0){
									if(empty($checkManualIT)){
										$insert=DB::insert("INSERT INTO `hrm_payscale` (`mas_ctc_id`,`ctc_group_id`,`company_id`,`location_id`,`payroll_group_id`,`u_name`,`data_name`,
										`From`,`To`,`monthly_value`,`yearly_value`,`Description`,`created_by`) VALUES ( '0', '1', '".$getEmpDatas[0]->company_id."', 
										'".$getEmpDatas[0]->location_id."', '".$getEmpDatas[0]->payroll_group_id."', '".$key5."','D008','".$MonthAndYear."',
										'".$MonthAndYear."','".$cur_month."','','IT auto generate from Income Tax module','".$user->emp_code."');");
									}
								}
								
								
							
			
							$delete_monpayr=DB::delete("DELETE FROM hrm_payroll_monpayr_incometax WHERE emp_code='".$key5."' AND monthandyear='".$MonthAndYear."' ");
			
							$insert_monpayr=DB::insert("INSERT INTO hrm_payroll_monpayr_incometax (emp_code,monthandyear,total_earning,total_approved_saving,net_taxable_income,total_tax_amount,current_month_tax,file,createdBy)
															VALUES ('".$key5."','".$MonthAndYear."','".$tot_earnings."','".intval(str_replace( ',', '',$final_data['approved_savings_total']))."','".intval(str_replace( ',', '',$final_data['net_taxable_income']))."',
															'".intval(str_replace( ',', '',$final_data['total_tax_amount']))."','".$cur_month."','".$file_name."','".$user->emp_code."') ");
							
						}
					}
				}
				/*incometax End*/

				$checkITDiff=DB::select("SELECT a.month,a.emp_code,a.amount,b.u_name,b.monthly_value 
														FROM hrm_payroll_monpayr_it_accounts_confirmation a 
														LEFT JOIN hrm_payscale b ON a.emp_code=b.u_name AND a.month=b.`From` AND a.month=b.`To`
														WHERE b.payroll_group_id='".$CompanyGroup_id."' AND a.month='".$MonthAndYear."' AND b.data_name='D008' AND a.amount !=b.monthly_value");
				$checkITDiff=json_decode(json_encode($checkITDiff), true);

				$curMonthTaxArray=array();

				foreach($checkITDiff as $key6 => $value6){
					$curMonthTaxArray[$key6]['emp_code']=$value6['emp_code'];
					$curMonthTaxArray[$key6]['accounts_confirmation_amount']=$value6['amount'];
					$curMonthTaxArray[$key6]['payroll_processed_amount']=$value6['monthly_value'];
					$curMonthTaxArray[$key6]['difference']=$value6['amount']-$value6['monthly_value'];
				}


				$AttendanceQry=DB::select("SELECT a.emp_code,CONCAT(date_format( DATE_SUB('".$MonthAndYear."-1', interval 1 month ), '%Y-%m-'),b.start_date) 'start_date',CONCAT(date_format('".$MonthAndYear."-1', '%Y-%m-'),b.end_date) 'end_date' 
											FROM hrm_profile a 
											INNER JOIN mas_attendance_cycle b ON a.attendance_cycle_id = b.id
											WHERE  a.company_id='".$Company_id."'  AND a.payroll_group_id='".$CompanyGroup_id."'");
				$AttendanceQry=json_decode(json_encode($AttendanceQry), true);

				$r=$AttendanceQry;
				for($i=0;$i<count($r);$i++){
					$attendance[$r[$i]['emp_code']]=$r[$i];
				}

				// $s18=db::select("SELECT  upper(p.u_name) 'u_name',
				// 					p.data_name 'Name', 
				// 					p.monthly_value 'Amount', p.Description,p.SpeDescription
				// 					FROM hrm_payscale as p 
				// 					WHERE p.status='1' $filter and company_id='".$Company_id."' and payroll_group_id='".$CompanyGroup_id."' 
				// 							and ( '".$MonthAndYear."' BETWEEN p.`From` and if(p.`To`='','".$MonthAndYear."', p.`To`) ) 
				// 					ORDER BY p.company_id ");
				$s18=db::select("SELECT 
									UPPER(p.u_name) AS u_name, 
									p.data_name AS Name, 
									p.monthly_value AS Amount, 
									p.Description, 
									p.effective_from_date,
									p.effective_to_date
									FROM hrm_payscale AS p
									WHERE p.status = '1'
									AND p.company_id = '1'
									AND p.payroll_group_id = '1'
									AND (
										'2025-09' BETWEEN p.`From` AND IF(p.`To` = '', '2025-09', p.`To`)
									)
									AND (
										'2025-08-21' BETWEEN p.effective_from_date AND p.effective_to_date
										OR '2025-09-20' BETWEEN p.effective_from_date AND p.effective_to_date
										OR (p.effective_from_date <= '2025-08-21' AND p.effective_to_date >= '2025-09-20')
									) 
									ORDER BY p.company_id, p.effective_from_date");
				$s18=json_decode(json_encode($s18), true);
			
				$s29=db::select("SELECT `Mode`, `Fields`, Name, LongName, PFAffected, PFAffectedMinus, ESIAffected, ADAAffected, Category, company_id,payroll_group_id ,category_of_emp, p.Ee
									FROM payscalemapping as p 
									WHERE p.company_id='".$Company_id."'  and  p.payroll_group_id='".$CompanyGroup_id."' 
									order by FIELD( p.`Mode`, 'Earning', 'Allowance', 'Deduction' ), p.OrderBy ");
				$s29=json_decode(json_encode($s29), true);

				$IPAdderess=$_SERVER["REMOTE_ADDR"];

				$s310=db::insert("insert into hrm_payscale_monpayr_setting ( MonthAndYear, company_id, payroll_group_id,category_of_emp, `Mode`, `Fields`, Name, LongName, OrderBy, 
									PFAffected, PFAffectedMinus, ESIAffected, ADAAffected, Category, Modified, payslip_standard_amt_flag, Ee, ViewOption, ACNO, GenerateUser, GenerateDate, GenerateIP )
									(
									select '".$MonthAndYear."',  company_id,  payroll_group_id,category_of_emp, `Mode`, `Fields`, p.Name, p.LongName, p.OrderBy , 
									p.PFAffected, p.PFAffectedMinus, p.ESIAffected, p.ADAAffected, p.Category, p.Modified,p.payslip_standard_amt_flag, p.Ee, ViewOption, p.ACNO, '".$request->user_name."', sysdate(), '".$IPAdderess."'
									FROM payscalemapping as p 
									WHERE p.company_id='".$Company_id."'  and  p.payroll_group_id='".$CompanyGroup_id."' 
									order by FIELD( p.`Mode`, 'Earning', 'Allowance', 'Deduction' ), p.OrderBy) ");
									$s310=json_decode(json_encode($s310), true);

				//PGStudents Hris Paygeneration Calulation days WD
				// original code $s411=db::select("SELECT day(LAST_DAY('".$MonthAndYear."-01')) 'Day' ");
				// shyad manual apply $s411 = [(object)['Day' => 31]];
				$s411 = [(object)['Day' => 31]];
				// $s411=db::select("select attendance_cycle from hrm_lop where MonthAndYear= '".$MonthAndYear."' GROUP BY attendance_cycle");
				
				list($start_date, $end_date) = explode(" to ", $s411[0]->attendance_cycle);
				$start_date = DateTime::createFromFormat('d-m-Y', trim($start_date));
				$end_date = DateTime::createFromFormat('d-m-Y', trim($end_date));
				if ($start_date && $end_date) {
					$interval = $start_date->diff($end_date);
					$days = $interval->days + 1; 
					$s411 =  [(object)[
						'Day' => $days
					]];
				} 
				$s411=json_decode(json_encode($s411), true);

				$s512=db::select("SELECT * FROM pf_no WHERE status='1' and payroll_group_id='".$CompanyGroup_id."' and company_id='".$Company_id."' and ( '".$MonthAndYear."' BETWEEN `from` and if(`to`='','".$MonthAndYear."', `to`) )");
				$s512=json_decode(json_encode($s512), true);

				$s613=db::select("SELECT * FROM payscalesettingmapping_pf WHERE status='1' and company_id='".$Company_id."'  and payroll_group_id='".$CompanyGroup_id."'  ");
				$s613=json_decode(json_encode($s613), true);

				$s714=db::insert("insert into hrm_payscale_monpayrbulkdata ( MonthAndYear, company_id, payroll_group_id, Data, `Values`, sysdate )
									(
										SELECT '".$MonthAndYear."',  company_id,  payroll_group_id, Data, `Values`, sysdate()
										FROM hrm_payscale_bulkdata as p 
										WHERE p.company_id='".$Company_id."' and payroll_group_id='".$CompanyGroup_id."' 
									)");
				$s714=json_decode(json_encode($s714), true);

				$payslip_query=DB::select("SELECT `Values`
											FROM hrm_payscale_bulkdata as p 
											WHERE p.company_id='".$Company_id."' and Data='PaySlipModel' and payroll_group_id='".$CompanyGroup_id."'");
				$payslip_query=json_decode(json_encode($payslip_query), true);
				$PaySlipModel=$payslip_query[0]['Values'];

				$s815=db::select("SELECT company_id, location_id, payroll_group_id, Method
									FROM payscale_salary_method as p 
									WHERE p.company_id='".$Company_id."' and p.payroll_group_id='".$CompanyGroup_id."' ");
				$s815=json_decode(json_encode($s815), true);

				$s916=db::select("SELECT `ModeSetting`, `Mode`, `Fields`, Name, LongName, PFAffected, PFAffectedMinus, ESIAffected, 
									ADAAffected, Category, Company, Location,CompanyGroup 
									FROM payscale_worker_mapping as p 
									WHERE p.Company='".$Company_id."'  and  p.CompanyGroup='".$CompanyGroup_id."' 
									order by FIELD( p.`Mode`, 'Earning', 'Allowance', 'Deduction' ), p.OrderBy");
				$s916=json_decode(json_encode($s916), true);

				$s1017=db::select("SELECT p.emp_code 'u_name', p.company_id,p.payroll_group_id, p.`Mode`, 
									sum(p.Days) 'Days', sum(p.`Hours`) 'Hours', sum(p.`Minutes`) 'Minutes' , p.Grade,
									if(p.EffMonthAndYear not in(''), day(LAST_DAY(concat(p.EffMonthAndYear,'-01'))), 0)  'TotalDays',
									p.EffMonthAndYear,hp.working_hours as WorkingHours
									FROM hrm_lop as p 
									LEFT JOIN hrm_profile hp on p.emp_code=hp.emp_code
									WHERE p.status='1' and p.company_id='".$Company_id."' and  p.payroll_group_id='".$CompanyGroup_id."' 
									and p.MonthAndYear='".$MonthAndYear."'
									group by p.emp_code, p.company_id,  p.payroll_group_id,p.Mode");
				$s1017=json_decode(json_encode($s1017), true);
			
				$s1118=db::select("SELECT company_id, location_id, payroll_group_id, `Mode`, SpeMode, NoOfDays, Percentage, Addition, `From`, `To`, Store
									FROM payscale_worker as p
									WHERE p.`status`='1' and p.company_id='".$Company_id."' and p.payroll_group_id='".$CompanyGroup_id."'
									and ( '".$MonthAndYear."' BETWEEN p.`From` and if(p.`To`='','".$MonthAndYear."', p.`To`) )");
				$s1118=json_decode(json_encode($s1118), true);

				$s1219=db::select("SELECT Company, CompanyGroup, Grade, Amount 
									FROM payscale_worker_acting as p
									WHERE p.`status`='1' and p.Company='".$Company_id."' and p.CompanyGroup='".$CompanyGroup_id."' 
											and ( '".$MonthAndYear."' BETWEEN p.`From` and if(p.`To`='','".$MonthAndYear."', p.`To`) )");
				$s1219=json_decode(json_encode($s1219), true);

				$s1320=db::select("SELECT company_id, payroll_group_id, Name, `Values`
									FROM payscale_basic as p
									where p.`status`='1' and p.company_id='".$Company_id."' and p.payroll_group_id='".$CompanyGroup_id."'
											and ( '".$MonthAndYear."' BETWEEN p.`From` and if(ifnull(p.`To`,'')='','".$MonthAndYear."', p.`To`) )");
				$s1320=json_decode(json_encode($s1320), true);

				$s1421=db::select("SELECT md.name 'dept_name',md.short_name'Allies' 
									FROM mas_department_map dp 
									LEFT JOIN mas_department md ON dp.department_id=md.id
									WHERE dp.company_id='".$Company_id."'");
				$s1421=json_decode(json_encode($s1421), true);

				$s2110=DB::Select("SELECT concat( MONTHNAME('".$MonthAndYear."-01'), ' - ', year('".$MonthAndYear."-01') ) 'MonthOF'" );
				$s2110=json_decode(json_encode($s2110), true);    

				$r=$s2110;
				for($i=0;$i<count($r);$i++)
				$MonthAndYearreport=$r[$i]['MonthOF'];

				$payscaleStaffProfile=array();
				$r=$s0;
				for($i=0;$i<count($r);$i++){
					$payscaleStaffProfile[$r[$i]['u_name']]=$r[$i];
				}
				$EmployeeList=0;
				$EmployeeList=count($payscaleStaffProfile);
				
				$PayScaleContainerArray=array();
				$r=$s18;
				for($i=0;$i<count($r);$i++){ 
					if($payscaleStaffProfile[$r[$i]['u_name']]){
						$PayScaleContainerArray[$r[$i]['u_name']] [$r[$i]['Name']]=array( 'Amount' => $r[$i]['Amount'], 'Description'=> $r[$i]['Description'],'SpeDescription'=> $r[$i]['SpeDescription'],'effective_from_date'=> $r[$i]['effective_from_date'],'effective_to_date'=> $r[$i]['effective_to_date']);
						
					}
				}
				
				// Initialize counters and lists
				$ActiveList=0;$HoldList=0;$ZeroSalaryList=0;
				$activelist=array();$holdlist=array();$zerolist=array();
				
				foreach ($payscaleStaffProfile as $u_name => $value) 
				{
					if($PayScaleContainerArray[$u_name]){
						if($value['preActive']==1) {
							$activelist[]['name']=$value['name'].' ('.$u_name.')';
							$ActiveList++;
						}
						if($value['preActive']==2) {
							$holdlist[]['name']=$value['name'].' ('.$u_name.')';
							$HoldList++;
						}
						if($value['preActive']==0) {
							$zerolist[]['name']=$value['name'].' ('.$u_name.')';
							$ZeroSalaryList++;
						}
					}
				}

				$r=$s0;
				for($i=0;$i<count($r);$i++){ 
					if(!isset($PayScaleContainerArray[$r[$i]['u_name']])){
						$Error[]['error']=$r[$i]['u_name']." : CTC Not Found";
					}
				}
			
				$PayscaleSettingArrray=array();
				$r=$s29;
				for($i=0;$i<count($r);$i++){ 
					$PayscaleSettingArrray[$r[$i]['company_id']] [$r[$i]['Mode']] [$r[$i]['Fields']] = array ( 'PFAffected' => $r[$i]['PFAffected'], 'PFAffectedMinus' => $r[$i]['PFAffectedMinus'],  'ESIAffected' => $r[$i]['ESIAffected'], 'ADAAffected' => $r[$i]['ADAAffected'], 'Ee' => $r[$i]['Ee'] ) ;
				}
				
				$nd=0;
				$r=$s411;
				for($i=0;$i<count($r);$i++){
					$nd=$r[$i]['Day'];
				}
				
				$r=$s512;
				for($i=0;$i<count($r);$i++){
					$individualCompanyPFArray[$r[$i]['pf_no']]=$r[$i];
					$payscale_Company_PF=$r[$i]['pf_no'];
				}

				$RoundOFFData=array();
				$r=$s613;
				for($i=0;$i<count($r);$i++){
					$RoundOFFData=array( 'DATA' => $r[$i]['DATA'],  'DATADem' => $r[$i]['DATADem'],  'PF' => $r[$i]['PF'],  'PFDem' => $r[$i]['PFDem'], 
					'PFBasic' => $r[$i]['PFBasic'], 'PFBasicDem' => $r[$i]['PFBasicDem'], 
					'ESI' => $r[$i]['ESI'],  'ESIDem' => $r[$i]['ESIDem'],  'NetRoundOff' => $r[$i]['NetRoundOff']);
				}

				$SalaryMethod=array();
				$r=$s815;
				for($i=0;$i<count($r);$i++){
					$SalaryMethod[$r[$i]['company_id']] [$r[$i]['location_id']] [$r[$i]['payroll_group_id']] = $r[$i]['Method'] ;
				}

				$WorkerPayrscaleSettingsArray=array();
				$r=$s916;
				for($i=0;$i<count($r);$i++){
					$WorkerPayrscaleSettingsArray[$r[$i]['Company']]  [$r[$i]['ModeSetting']] [$r[$i]['Mode']] [$r[$i]['Fields']] = array ( 'PFAffected' => $r[$i]['PFAffected'],  'PFAffectedMinus' => $r[$i]['PFAffectedMinus'],  'ESIAffected' => $r[$i]['ESIAffected'], 'ADAAffected' => $r[$i]['ADAAffected'] ) ;
				}

				$AttendanceDetails=array();
				$r=$s1017;
				for($i=0;$i<count($r);$i++){
					$AttendanceDetails[$r[$i]['company_id']]  [$r[$i]['payroll_group_id']] [$r[$i]['Mode']] [$r[$i]['u_name']] = 
					array ( 'Days' => $r[$i]['Days'], 'Hours' => $r[$i]['Hours'], 'Minutes' => $r[$i]['Minutes'], 'WorkingHours' => $r[$i]['WorkingHours'], 'Grade' => $r[$i]['Grade'],
					'TotalDays' => $r[$i]['TotalDays'], 'EffMonthAndYear' => $r[$i]['EffMonthAndYear']) ;
				}
				
				$PayscaleWorkerDetails=array();
				$r=$s1118;
				for($i=0;$i<count($r);$i++){
					$PayscaleWorkerDetails[$r[$i]['company_id']] [$r[$i]['location_id']] [$r[$i]['payroll_group_id']] [$r[$i]['Mode']] = 
					array ( 'SpeMode' => $r[$i]['SpeMode'], 'NoOfDays' => $r[$i]['NoOfDays'], 'Percentage' => $r[$i]['Percentage'],  'Addition' => $r[$i]['Addition'], 'Store' => $r[$i]['Store']) ;
				}
			
				$PayscaleWorkerActing=array();
				$r=$s1219;
				for($i=0;$i<count($r);$i++){
					$PayscaleWorkerActing[$r[$i]['Company']][$r[$i]['CompanyGroup']] [$r[$i]['Grade']] = $r[$i]['Amount'] ;
				}

				$PayscaleBasic=array();
				$r=$s1320;
				for($i=0;$i<count($r);$i++){
					$PayscaleBasic[$r[$i]['company_id']]  [$r[$i]['payroll_group_id']] [$r[$i]['Name']] = $r[$i]['Values'] ;
				}					

				$DeptMaster=array();
				$r=$s1421;
				for($i=0;$i<count($r);$i++){
					$DeptMaster[$r[$i]['dept_name']] = $r[$i]['Allies'] ;
				}	
				
				if($payscaleStaffProfile)
				{
					if($PayScaleContainerArray)
					{
						$MinusNet=array();
						$Sno=150;
						$ZeroSalary=0;
						$Increment=1;
						$IncrementArray=array();
						$IncrementArray[]=1;
						
						foreach( $payscaleStaffProfile as $payscaleStaffProfileIndex => $payscaleStaffProfileValue )
						{
							$matchCompanyPFForSettings=$payscale_Company_PF;

							if($individualCompanyPFArray[$matchCompanyPFForSettings])
							{
								$rawRaw=$individualCompanyPFArray[$matchCompanyPFForSettings];
								$payscaleStaffProfileValue['empno'].'----'.$company_pf_no =$rawRaw['pf_no'].'-----';						
								$pf_per=$rawRaw['pf'];
								$ErPFPer=$rawRaw['ErPF'];
								$ErPensionPer=$rawRaw['ErPension'];
								$ErPensionMax=$rawRaw['ErPensionMax'];
								$ac2_per=$rawRaw['ac2'];
								$ac21_per=$rawRaw['ac21'];
								$ac22_per=$rawRaw['ac22'];
								$ac10_per=$rawRaw['ac10'];
								$ESIEligible=$rawRaw['ESIEligible'];
								$esi_per=$rawRaw['esi_per'];
								$esi_per_o=$rawRaw['esi_per_o'];
								$PF_Limit=$rawRaw['PFLimit'];
							}

							$Sno++;
							if($Sno%250==0){
								$Increment++;
								$IncrementArray[]=$Increment;
							}

							if($PayScaleContainerArray[$payscaleStaffProfileIndex] )
							{
								unset($ExtraData,$NetSalary,$RoundOff,$TotalDeduction,$Gross,$TotalSalary,$PFBasicAffected,$IncomeTaxPercentage,$IncomeShow,$lopAmount,$lop_deduction,$lophour,$lopDetected,$pd,$ctcvalue,$ctcActual);
								
								//note 2
								$u_name=$payscaleStaffProfileIndex;

								if($attendance[$u_name]){
									$worked_days_Qry=DB::select("SELECT COUNT(*)-sum(ha.pay_check) 'LOP',ha.emp_code 
																FROM hrm_attendance ha
																LEFT JOIN hrm_profile hp ON hp.emp_code=ha.emp_code 
																WHERE ha.attendance_date between '".$attendance[$u_name]['start_date']."' and '".$attendance[$u_name]['end_date']."' 
																		and hp.emp_code='".$u_name."'");
									$worked_days_Qry=json_decode(json_encode($worked_days_Qry), true);
								}
								
								$Company=$payscaleStaffProfileValue['Company'];
								$Company_id=$payscaleStaffProfileValue['company_id'];
								$Location_id=$payscaleStaffProfileValue['location_id'];
								$Location=$payscaleStaffProfileValue['Location'];
								$CompanyGroup=$payscaleStaffProfileValue['payroll_group_id'];								
								$CategoryOfEmp=$payscaleStaffProfileValue['category_of_emp'];
								
								// Automatic Stipend Salary Calculation Enhancement
								// Removed category condition - will run for all employees
									
									// Calculate payroll cycle dates (21st of previous month to 20th of current month)
									$month_year = explode('-', $MonthAndYear);
									$year = $month_year[0];
									$month = $month_year[1];
									
									// Previous month calculation
									$prev_month = $month - 1;
									$prev_year = $year;
									if($prev_month == 0) {
										$prev_month = 12;
										$prev_year = $year - 1;
									}
									
									$payroll_cycle_start = sprintf('%04d-%02d-21', $prev_year, $prev_month);
									$payroll_cycle_end = sprintf('%04d-%02d-20', $year, $month);
									
									// Get payscale periods for the employee from hrm_payscale table
									$payscale_periods = DB::select("SELECT DISTINCT
																		UPPER(p.u_name) AS u_name, 
																		p.data_name AS Name, 
																		p.monthly_value AS Amount, 
																		p.yearly_value AS YearlyAmount,
																		p.Description, 
																		p.effective_from_date,
																		p.effective_to_date
																		FROM hrm_payscale AS p
																		WHERE p.status = '1'
																		AND p.u_name = ?
																		AND p.company_id = ?
																		AND p.payroll_group_id = ?
																		AND (
																			? BETWEEN p.`From` AND IF(p.`To` = '', ?, p.`To`)
																		)
																		AND p.data_name = 'E001'
																		AND p.effective_from_date <= ?
																		AND p.effective_to_date >= ?
																		ORDER BY p.effective_from_date ASC", 
																		[$u_name, $Company_id, $CompanyGroup, $MonthAndYear, $MonthAndYear, 
																		 $payroll_cycle_end, $payroll_cycle_start]);
									
									// Get arrears amount (EA001) from hrm_payscale table
									$arrears_data = DB::select("SELECT 
																	UPPER(p.u_name) AS u_name, 
																	p.data_name AS Name, 
																	p.monthly_value AS Amount, 
																	p.yearly_value AS YearlyAmount,
																	p.Description
																	FROM hrm_payscale AS p
																	WHERE p.status = '1'
																	AND p.u_name = ?
																	AND p.company_id = ?
																	AND p.payroll_group_id = ?
																	AND p.data_name = 'EA001'
																	AND (
																		? BETWEEN p.`From` AND IF(p.`To` = '', ?, p.`To`)
																	)", 
																	[$u_name, $Company_id, $CompanyGroup, $MonthAndYear, $MonthAndYear]);
									
									$payscale_periods = json_decode(json_encode($payscale_periods), true);
									$arrears_data = json_decode(json_encode($arrears_data), true);
									
									// Calculate arrears amount
									$arrears_amount = 0;
									if(!empty($arrears_data)) {
										$arrears_amount = $arrears_data[0]['Amount'] ?? 0;
									}
									
									if(!empty($payscale_periods)) {
										$salary_segments = [];
										$total_working_days = 0;
										
										// Calculate total working days in payroll cycle
										$start_date = new DateTime($payroll_cycle_start);
										$end_date = new DateTime($payroll_cycle_end);
										$total_cycle_days = $start_date->diff($end_date)->days + 1;
										
										// Get LOP data first to calculate actual working days
										$lop_data = DB::select("SELECT old_lop, new_lop, total_work_days, Days 
																FROM hrm_lop 
																WHERE emp_code = ? 
																AND MonthAndYear = ? 
																AND company_id = ? 
																AND payroll_group_id = ?", 
																[$u_name, $MonthAndYear, $Company_id, $CompanyGroup]);
										
										$lop_data = json_decode(json_encode($lop_data), true);
										$old_lop = 0;
										$new_lop = 0;
										$lop_days = 0;
										
										if(!empty($lop_data)) {
											$lop_record = $lop_data[0];
											$old_lop = $lop_record['old_lop'] ?? 0;
											$new_lop = $lop_record['new_lop'] ?? 0;
											$lop_days = $lop_record['Days'] ?? 0;
										}
										
										// Calculate PD (Present Days) for hrm_payscale_monpayr_details
										$pd_days = 0;
										if(!empty($lop_data)) {
											// Days column in hrm_lop table contains LOP days
											// PD = Total working days (31) - LOP days
											$pd_days = $total_cycle_days - $lop_days;
										} else {
											// If no LOP data, assume full working days
											$pd_days = $total_cycle_days;
										}
										
										// Split payroll cycle across payscale periods
										foreach($payscale_periods as $payscale_period) {
											$payscale_start = new DateTime($payscale_period['effective_from_date']);
											$payscale_end = new DateTime($payscale_period['effective_to_date']);
											$payroll_start = new DateTime($payroll_cycle_start);
											$payroll_end = new DateTime($payroll_cycle_end);
											
											// Find intersection of payscale period and payroll cycle
											$segment_start = max($payscale_start, $payroll_start);
											$segment_end = min($payscale_end, $payroll_end);
											
											if($segment_start <= $segment_end) {
												$total_segment_days = $segment_start->diff($segment_end)->days + 1;
												$monthly_salary = $payscale_period['Amount'];
												$yearly_salary = $payscale_period['YearlyAmount'];
												
												// Calculate actual working days by subtracting LOP
												$working_days = $total_segment_days;
												
												// Check if this is a single segment covering the entire payroll cycle
												$is_full_cycle_segment = ($segment_start <= $payroll_start && $segment_end >= $payroll_end);
												
												if($is_full_cycle_segment) {
													// For single segment covering full cycle, apply total LOP (old_lop + new_lop)
													$total_lop = $old_lop + $new_lop;
													$working_days = $total_segment_days - $total_lop;
												} else {
													// For multiple segments, apply LOP based on segment position
													// Apply old_lop to first segment (lowest effective_from_date)
													// Apply new_lop to last segment (highest effective_from_date)
													
													// Check if this is the first segment (earliest effective_from_date)
													$is_first_segment = ($payscale_period['effective_from_date'] == min(array_column($payscale_periods, 'effective_from_date')));
													
													// Check if this is the last segment (latest effective_from_date)
													$is_last_segment = ($payscale_period['effective_from_date'] == max(array_column($payscale_periods, 'effective_from_date')));
													
													if($is_first_segment && $old_lop > 0) {
														$working_days = $total_segment_days - $old_lop;
													} else if($is_last_segment && $new_lop > 0) {
														$working_days = $total_segment_days - $new_lop;
													}
													// For middle segments (if any), no LOP applied
													// working_days remains as total_segment_days
												}
												
												// Ensure working days is not negative
												$working_days = max(0, $working_days);
												
												// Pro-rate salary based on actual working days
												$pro_rated_salary = ($monthly_salary / 31) * $working_days;
												
												$salary_segments[] = [
													'payscale_id' => $payscale_period['Name'],
													'period_start' => $segment_start->format('Y-m-d'),
													'period_end' => $segment_end->format('Y-m-d'),
													'total_days' => $total_segment_days,
													'working_days' => $working_days,
													'monthly_salary' => $monthly_salary,
													'yearly_salary' => $yearly_salary,
													'pro_rated_salary' => round($pro_rated_salary, 2)
												];
												
												$total_working_days += $working_days;
												
										// Debug: Log segment details (can be removed in production)
										// error_log("Employee " . $u_name . " - Segment: " . $segment_start->format('Y-m-d') . " to " . $segment_end->format('Y-m-d') . 
										// 		 " | Total days: " . $total_segment_days . " | Working days: " . $working_days . 
										// 		 " | Monthly salary: " . $monthly_salary . " | Is full cycle: " . ($is_full_cycle_segment ? 'Yes' : 'No') .
										// 		 " | Is first segment: " . ($is_first_segment ? 'Yes' : 'No') . " | Is last segment: " . ($is_last_segment ? 'Yes' : 'No'));
											}
										}
										
										// Debug: Log total segments created (can be removed in production)
										// error_log("Employee " . $u_name . " - Total segments created: " . count($salary_segments));
										
									// Check if this is a 2-period salary change case (old_lop > 0 AND new_lop > 0)
									$is_salary_change_case = ($old_lop > 0 && $new_lop > 0);
									
									// Additional check: Only create D002 if we have exactly 2 different salary periods
									$unique_periods = [];
									foreach($payscale_periods as $period) {
										$key = $period['effective_from_date'] . '_' . $period['effective_to_date'];
										if(!isset($unique_periods[$key])) {
											$unique_periods[$key] = $period;
										}
									}
									$unique_period_count = count($unique_periods);
									
									// Create D002 if we have exactly 2 unique periods (regardless of LOP values)
									// This handles salary change cases even when LOP is 0 or only one LOP value is present
									$should_create_d002 = ($unique_period_count == 2);
										
										// Debug: Log payscale periods and LOP data
										// Debug: Log payscale analysis (can be removed in production)
										// error_log("Employee " . $u_name . " - Payscale periods found: " . count($payscale_periods));
										// error_log("Employee " . $u_name . " - Unique periods: " . $unique_period_count);
										// error_log("Employee " . $u_name . " - LOP data: old_lop=" . $old_lop . ", new_lop=" . $new_lop . ", is_salary_change_case=" . ($is_salary_change_case ? 'Yes' : 'No'));
										// error_log("Employee " . $u_name . " - Should create D002: " . ($should_create_d002 ? 'Yes' : 'No'));
										
										// Comprehensive LOP calculation logic for all user cases
										if(!empty($lop_data)) {
											$lop_record = $lop_data[0];
											$total_work_days = $lop_record['total_work_days'] ?? $total_cycle_days;
											
											// Check number of payscale segments to determine LOP logic
											$segment_count = count($salary_segments);
											
											// Case 1: Both old_lop and new_lop are 0 - use Days column from hrm_lop
											if($old_lop == 0 && $new_lop == 0) {
												$lop_days = $lop_record['Days'] ?? 0;
												
												if($lop_days > 0 && !empty($salary_segments)) {
													// Has LOP - calculate present days
													$first_segment = $salary_segments[0];
													$daily_rate = $first_segment['monthly_salary'] / 31;
													$lop_deduction = $lop_days * $daily_rate;
													
													$present_days = $total_cycle_days - $lop_days;
													$d001_amount = $present_days * $daily_rate;
													$d002_amount = 0;
												} else if($lop_days == 0 && !empty($salary_segments)) {
													// No LOP - full present days
													$first_segment = $salary_segments[0];
													$daily_rate = $first_segment['monthly_salary'] / 31;
													$d001_amount = $total_cycle_days * $daily_rate;
													$d002_amount = 0;
													$lop_deduction = 0;
												}
											}
											// Case 2: Salary change case (exactly 2 unique periods) - create D001 and D002
											else if($should_create_d002) {
												// Calculate D001 amount (present days for first period)
												if(!empty($salary_segments)) {
													$first_segment = $salary_segments[0];
													$daily_rate = $first_segment['monthly_salary'] / 31;
													$d001_amount = $first_segment['working_days'] * $daily_rate;
												}
												
												// Calculate D002 amount (present days for second period)
												if(count($salary_segments) >= 2) {
													$last_segment = end($salary_segments);
													$daily_rate = $last_segment['monthly_salary'] / 31;
													$d002_amount = $last_segment['working_days'] * $daily_rate;
												}
												
												// Calculate LOP deduction for lopAmount in details table
												$old_lop_amount = $old_lop * ($first_segment['monthly_salary'] / 31);
												$new_lop_amount = $new_lop * ($last_segment['monthly_salary'] / 31);
												$lop_deduction = $old_lop_amount + $new_lop_amount;
											}
											// Case 3: Single segment with old_lop > 0 (but new_lop = 0)
											else if($segment_count == 1 && $old_lop > 0 && $new_lop == 0) {
												if(!empty($salary_segments)) {
													$first_segment = $salary_segments[0];
													$daily_rate = $first_segment['monthly_salary'] / 31;
													$d001_amount = $first_segment['working_days'] * $daily_rate;
												}
												
												$d002_amount = 0;
												$lop_deduction = $old_lop * ($first_segment['monthly_salary'] / 31);
											}
											// Case 4: Single segment with new_lop > 0 (but old_lop = 0)
											else if($segment_count == 1 && $old_lop == 0 && $new_lop > 0) {
												if(!empty($salary_segments)) {
													$first_segment = $salary_segments[0];
													$daily_rate = $first_segment['monthly_salary'] / 31;
													$d001_amount = $first_segment['working_days'] * $daily_rate;
												}
												
												$d002_amount = 0;
												$lop_deduction = $new_lop * ($first_segment['monthly_salary'] / 31);
											}
											// Case 5: Single segment with both old_lop > 0 AND new_lop > 0
											else if($segment_count == 1 && $old_lop > 0 && $new_lop > 0) {
												if(!empty($salary_segments)) {
													$first_segment = $salary_segments[0];
													$daily_rate = $first_segment['monthly_salary'] / 31;
													$d001_amount = $first_segment['working_days'] * $daily_rate;
												}
												
												$d002_amount = 0;
												$lop_deduction = ($old_lop + $new_lop) * ($first_segment['monthly_salary'] / 31);
											}
											// Case 6: Default case - single segment, no LOP or fallback
											else {
												if(!empty($salary_segments)) {
													$first_segment = $salary_segments[0];
													$daily_rate = $first_segment['monthly_salary'] / 31;
													
													// Use working_days from segment (already has LOP applied in segment creation)
													$d001_amount = $first_segment['working_days'] * $daily_rate;
													
													// Calculate LOP deduction based on available LOP data
													if($old_lop > 0) {
														$lop_deduction = $old_lop * $daily_rate;
													} else if($new_lop > 0) {
														$lop_deduction = $new_lop * $daily_rate;
													} else {
														$lop_days = $lop_record['Days'] ?? 0;
														$lop_deduction = $lop_days * $daily_rate;
													}
												}
												
												$d002_amount = 0;
											}
										} else {
											// No LOP data - use full cycle days
											if(!empty($salary_segments)) {
												$first_segment = $salary_segments[0];
												$daily_rate = $first_segment['monthly_salary'] / 31;
												$d001_amount = $total_cycle_days * $daily_rate;
												$d002_amount = 0;
												$lop_deduction = 0;
											}
										}
										
										// Calculate E001Grossnet as sum of D001 + D002 + Arrears
										$final_salary = $d001_amount + $d002_amount + $arrears_amount;
										
										// Debug: Log final calculation results (can be removed in production)
										// error_log("Employee " . $u_name . " - Final Results: D001=" . round($d001_amount, 2) . 
										// 		 ", D002=" . round($d002_amount, 2) . ", Arrears=" . round($arrears_amount, 2) . 
										// 		 ", E001Grossnet=" . round($final_salary, 2) . ", Segment Count=" . count($salary_segments) . 
										// 		 ", PD Days=" . $pd_days . ", Total Cycle Days=" . $total_cycle_days . 
										// 		 ", LOP Days=" . $lop_days . ", Old LOP=" . $old_lop . ", New LOP=" . $new_lop);
										
										// Insert into hrm_payscale_monpayr_details with all employee data
										$details_insert = DB::insert("INSERT INTO hrm_payscale_monpayr_details 
																		(MonthAndYear, u_name, company_id, division_id, location_id, payroll_group_id, 
																		 category_of_emp, EmpNo, Name, FatherName, Gender, Dept, Designation, 
																		 DOB, DOJ, DOR, off_mail_id, payslip_model, payslip_block, CompanyPFNo, 
																		 EmpESINO, EmpPFNO, WorkLocation, WorkLevel, CostCodeName, PANNo, 
																		 BankAcNo, BankName, SlabName, BankIFSC, VPFPer, GradeName, 
																		 ESICalculation, ESIActive, PFCalculation, LOPAmountAmount, LOPHourAmount, 
																		 LOPHour, LOPAmount, PD, WD, UAN, Active, preActive, PDDays, Status, Sync) 
																		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																		[$MonthAndYear, $u_name, $Company_id, $payscaleStaffProfileValue['division_id'] ?? null, $Location_id, $CompanyGroup, 
																		 $CategoryOfEmp, $payscaleStaffProfileValue['empno'] ?? '0', $payscaleStaffProfileValue['name'] ?? '0', 
																		 $payscaleStaffProfileValue['father_name'] ?? '0', $payscaleStaffProfileValue['gender'] ?? '0', 
																		 $payscaleStaffProfileValue['dept'] ?? '0', $payscaleStaffProfileValue['designation'] ?? '0', 
																		 $payscaleStaffProfileValue['DOJ'] ?? null, $payscaleStaffProfileValue['date_of_join'] ?? null, 
																		 $payscaleStaffProfileValue['DOR'] ?? null, $payscaleStaffProfileValue['off_mail_id'] ?? null, 
																		 $payscaleStaffProfileValue['payslip_model'] ?? 0, $payscaleStaffProfileValue['payslip_block'] ?? 0, 
																		 $payscaleStaffProfileValue['company_pf_no'] ?? '0', $payscaleStaffProfileValue['emp_esi_no'] ?? '0', 
																		 $payscaleStaffProfileValue['emp_pf_no'] ?? '0', $payscaleStaffProfileValue['work_location'] ?? null, 
																		 $payscaleStaffProfileValue['work_level'] ?? null, $payscaleStaffProfileValue['cost_code_name'] ?? '0', 
																		 $payscaleStaffProfileValue['PANNo'] ?? '0', $payscaleStaffProfileValue['BankAcNo'] ?? '0', 
																		 $payscaleStaffProfileValue['BankName'] ?? '0', $payscaleStaffProfileValue['SlabName'] ?? '0', 
																		 $payscaleStaffProfileValue['BankIFSC'] ?? '0', $payscaleStaffProfileValue['VPFPercentage'] ?? 0.00, 
																		 $payscaleStaffProfileValue['grade_name'] ?? '0', $payscaleStaffProfileValue['esi_calculation'] ?? 0, 
																		 $payscaleStaffProfileValue['esi_active'] ?? 0, $payscaleStaffProfileValue['pf_calculation'] ?? 0, 
																		 0, 0, 0, round($lop_deduction, 2), $pd_days, $total_cycle_days, 
																		 $payscaleStaffProfileValue['uan'] ?? null, $payscaleStaffProfileValue['active'] ?? '0', 
																		 $payscaleStaffProfileValue['pre_active'] ?? '0', '0', 1, 0]);
										
										// Insert salary segments into hrm_payscale_monpayr (single record with sum)
										$total_pro_rated_salary = array_sum(array_column($salary_segments, 'pro_rated_salary'));
										$total_monthly_salary = array_sum(array_column($salary_segments, 'monthly_salary'));
										
										// Create description with all periods
										$period_descriptions = [];
										foreach($salary_segments as $segment) {
											$period_descriptions[] = $segment['period_start'] . ' to ' . $segment['period_end'] . ' (' . $segment['working_days'] . ' days)';
										}
										$description = 'Salary - ' . implode(', ', $period_descriptions);
										
										// Use D001 + D002 amount instead of total_pro_rated_salary for E001
										$e001_amount = $d001_amount + $d002_amount;
										
										// Get last segment's monthly salary for Actual value
										$last_segment_monthly_salary = !empty($salary_segments) ? end($salary_segments)['monthly_salary'] : 0;
										
										$segment_insert = DB::insert("INSERT INTO hrm_payscale_monpayr 
																			(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
																			 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
																			 Description, SpeDescription, preActive) 
																			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																			[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
																			 $CategoryOfEmp, 'E001', round($e001_amount, 2), 
																			 round($last_segment_monthly_salary, 2), 0, 0, 
																			 $description, 'Auto Generated', 1]);
										
										// Insert LOP deductions separately - comprehensive logic for all cases
										if(!empty($lop_data)) {
											$lop_record = $lop_data[0];
											$old_lop = $lop_record['old_lop'] ?? 0;
											$new_lop = $lop_record['new_lop'] ?? 0;
											
											// Check number of payscale segments to determine insert logic
											$segment_count = count($salary_segments);
											
											// Case 1: Both old_lop and new_lop are 0 - insert single D001 record
											if($old_lop == 0 && $new_lop == 0 && $d001_amount > 0) {
												$first_segment = $salary_segments[0];
												$present_days = $total_cycle_days - ($lop_record['Days'] ?? 0);
												DB::insert("INSERT INTO hrm_payscale_monpayr 
															(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
															 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
															 Description, SpeDescription, preActive) 
															VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
															[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
															 $CategoryOfEmp, 'D001', round($d001_amount, 2), 
															 round($d001_amount, 2), 0, 0, 
															 'Present Days - ' . $present_days . ' days', 'Auto Generated', 1]);
											}
											// Case 2: Salary change case - insert D001 and D002 records
											else if($should_create_d002) {
												// Insert D001 for first period (present days)
												if($d001_amount > 0) {
													$first_segment = $salary_segments[0];
													DB::insert("INSERT INTO hrm_payscale_monpayr 
																(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
																 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
																 Description, SpeDescription, preActive) 
																VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
																 $CategoryOfEmp, 'D001', round($d001_amount, 2), 
																 round($d001_amount, 2), 0, 0, 
																 'Present Days - ' . $first_segment['working_days'] . ' days', 'Auto Generated', 1]);
												}
												
												// Insert D002 for second period (present days)
												if($d002_amount > 0) {
													$last_segment = end($salary_segments);
													DB::insert("INSERT INTO hrm_payscale_monpayr 
																(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
																 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
																 Description, SpeDescription, preActive) 
																VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
																 $CategoryOfEmp, 'D002', round($d002_amount, 2), 
																 round($d002_amount, 2), 0, 0, 
																 'Present Days - ' . $last_segment['working_days'] . ' days', 'Auto Generated', 1]);
												}
											}
											// Case 3: Single segment with old_lop > 0 (but new_lop = 0)
											else if($segment_count == 1 && $old_lop > 0 && $new_lop == 0) {
												if($d001_amount > 0) {
													$first_segment = $salary_segments[0];
													DB::insert("INSERT INTO hrm_payscale_monpayr 
																(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
																 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
																 Description, SpeDescription, preActive) 
																VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
																 $CategoryOfEmp, 'D001', round($d001_amount, 2), 
																 round($d001_amount, 2), 0, 0, 
																 'Present Days - ' . $first_segment['working_days'] . ' days', 'Auto Generated', 1]);
												}
											}
											// Case 4: Single segment with new_lop > 0 (but old_lop = 0)
											else if($segment_count == 1 && $old_lop == 0 && $new_lop > 0) {
												if($d001_amount > 0) {
													$first_segment = $salary_segments[0];
													DB::insert("INSERT INTO hrm_payscale_monpayr 
																(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
																 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
																 Description, SpeDescription, preActive) 
																VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
																 $CategoryOfEmp, 'D001', round($d001_amount, 2), 
																 round($d001_amount, 2), 0, 0, 
																 'Present Days - ' . $first_segment['working_days'] . ' days', 'Auto Generated', 1]);
												}
											}
											// Case 5: Single segment with both old_lop > 0 AND new_lop > 0
											else if($segment_count == 1 && $old_lop > 0 && $new_lop > 0) {
												if($d001_amount > 0) {
													$first_segment = $salary_segments[0];
													DB::insert("INSERT INTO hrm_payscale_monpayr 
																(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
																 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
																 Description, SpeDescription, preActive) 
																VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
																 $CategoryOfEmp, 'D001', round($d001_amount, 2), 
																 round($d001_amount, 2), 0, 0, 
																 'Present Days - ' . $first_segment['working_days'] . ' days', 'Auto Generated', 1]);
												}
											}
											// Case 6: Default case - single segment, no LOP or fallback
											else {
												if($d001_amount > 0) {
													$first_segment = $salary_segments[0];
													DB::insert("INSERT INTO hrm_payscale_monpayr 
																(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
																 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
																 Description, SpeDescription, preActive) 
																VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
																[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
																 $CategoryOfEmp, 'D001', round($d001_amount, 2), 
																 round($d001_amount, 2), 0, 0, 
																 'Present Days - ' . $first_segment['working_days'] . ' days', 'Auto Generated', 1]);
												}
											}
										} else {
											// No LOP data - insert D001 with full cycle days
											if($d001_amount > 0) {
												DB::insert("INSERT INTO hrm_payscale_monpayr 
															(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
															 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
															 Description, SpeDescription, preActive) 
															VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
															[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
															 $CategoryOfEmp, 'D001', round($d001_amount, 2), 
															 round($d001_amount, 2), 0, 0, 
															 'Present Days - ' . $total_cycle_days . ' days', 'Auto Generated', 1]);
											}
										}
										
										// Insert arrears amount if exists
										if($arrears_amount > 0) {
											DB::insert("INSERT INTO hrm_payscale_monpayr 
														(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
														 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
														 Description, SpeDescription, preActive) 
														VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
														[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
														 $CategoryOfEmp, 'EA001', round($arrears_amount, 2), 
														 round($arrears_amount, 2), 0, 0, 
														 'Arrears Amount', 'Auto Generated', 1]);
										}
										
										// Insert total gross salary with E001Grossnet DataName (sum of D001 + D002 + Arrears)
										DB::insert("INSERT INTO hrm_payscale_monpayr 
													(MonthAndYear, u_name, company_id, location_id, payroll_group_id, 
													 category_of_emp, DataName, `Values`, Actual, Pre, Per, 
													 Description, SpeDescription, preActive) 
													VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
													[$MonthAndYear, $u_name, $Company_id, $Location_id, $CompanyGroup, 
													 $CategoryOfEmp, 'E001Grossnet', round($final_salary, 2), 
													 round($d001_amount + $d002_amount + $arrears_amount, 2), 0, 0, 
													 'Total Salary (D001 + D002 + Arrears)', 'Auto Generated', 1]);
										
										// Log successful calculation with detailed breakdown
										$log_message = "Salary calculated: " . $u_name . " | D001: " . round($d001_amount, 2) . 
													 " | D002: " . round($d002_amount, 2) . " | Arrears: " . round($arrears_amount, 2) . 
													 " | E001Grossnet: " . round($final_salary, 2) . " | PD: " . $pd_days . " | WD: " . $total_cycle_days;
										
										if(!empty($lop_data)) {
											$lop_record = $lop_data[0];
											$old_lop = $lop_record['old_lop'] ?? 0;
											$new_lop = $lop_record['new_lop'] ?? 0;
											
											if($old_lop > 0) {
												$log_message .= " | Old LOP (" . $old_lop . " days): " . round($old_lop_amount, 2);
											}
											
											if($new_lop > 0) {
												$log_message .= " | New LOP (" . $new_lop . " days): " . round($new_lop_amount, 2);
											}
										}
										
										error_log($log_message);
										
										// Skip normal payroll calculation for employees with payscale data
										continue;
										
									} else {
										$Error[]['error'] = 'No payscale data found for employee: ' . $u_name;
										continue;
									}
								
								$WorkLocation=$payscaleStaffProfileValue['WorkLocation'];
								$empno=$payscaleStaffProfileValue['empno'];
								$name=$payscaleStaffProfileValue['name'];
								$dept=$payscaleStaffProfileValue['dept'];
								$doj=$payscaleStaffProfileValue['date_of_join'];
								$designation=$payscaleStaffProfileValue['designation'];
								$dob=$payscaleStaffProfileValue['dob'];
								$AGE=$payscaleStaffProfileValue['AGE'];
								$date_of_join=$payscaleStaffProfileValue['date_of_join'];
								$WorkedDays =$payscaleStaffProfileValue['WorkedDays'];
								$DOR='';
								if(isset($payscaleStaffProfileValue['DOR']))
								$DOR=$payscaleStaffProfileValue['DOR'];								
								$father_name=$payscaleStaffProfileValue['father_name'];
								$division=$payscaleStaffProfileValue['divition'];
								$Active=$payscaleStaffProfileValue['active'];
								$preActive=$payscaleStaffProfileValue['preActive'];
								$gender=$payscaleStaffProfileValue['gender'];
								$StaffEPSActive =$payscaleStaffProfileValue['EPS'];
								$UAN =$payscaleStaffProfileValue['UAN'];

								$IncomeShow=0;
								if(isset($payscaleStaffProfileValue['IncomeShow']))
								$IncomeShow=$payscaleStaffProfileValue['IncomeShow'];
								if(isset($payscaleStaffProfileValue['IncomeTaxPercentage']))
								$IncomeTaxPercentage=$payscaleStaffProfileValue['IncomeTaxPercentage'];
								$Emp_Type=$payscaleStaffProfileValue['employe_type'];

								$PayscaleDataContainer=array();
								$PFBasic=0;
								$PFBasicMinus=0;
								$ESIBasic=0;
								$ADABasic=0;
								$PFBasicArrear=0;
								$PFBasicArrearMinus=0;
								$ESIBasicArrear=0;
								$ADABasicArrear=0;
								
								if($PayscaleSettingArrray[$Company_id]){
									foreach($PayscaleSettingArrray[$Company_id]  as $Index => $ModeArray)
									{
										foreach($ModeArray  as $ModeIndex => $EarningAddValue)
										{
											if(!isset($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']))
												$PayScaleContainerArray[$u_name][$ModeIndex]['Amount']=0;

											if(is_numeric($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'])){
												$PayscaleDataContainer[$Index][$ModeIndex]=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];

												if($EarningAddValue['PFAffected']){
													if($Index=='Allowance')
														$PFBasicArrear +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
													else
														$PFBasic +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
												}

												if($EarningAddValue['PFAffectedMinus']){
													if($Index=='Allowance')
														$PFBasicArrearMinus +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
													else
														$PFBasicMinus +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
												}

												if($EarningAddValue['ESIAffected'])
													$ESIBasic +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
												else if($ModeIndex=='E004' and $Company=='Chettinad Cement Corporation Limited')
													$ESIBasic +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
												
												if($EarningAddValue['ADAAffected'])
												$ADABasic +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
											}
											else
												$PayscaleDataContainer[$Index][$ModeIndex]=0;
										}
									}
								}
								else{
									$generateArray['data']="no setting process";
									$generateArray['info']=" Please Refer Setting for Payroll Process, Setting Mapping Yet not Done";
									return $generateArray;
								}


								if(is_array($PayscaleDataContainer['Earning']))
									$GrossSalary=array_sum($PayscaleDataContainer['Earning']);
								else
									$GrossSalary=0;
									$GrossSalaryForESI=$GrossSalary;
									
									$TotalSalary=$this->PaygenerateRoundOff( $GrossSalary, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
									

								#paygen-start-001
								if($TotalSalary && $preActive)
								{	 		
									$ADAOrg=0;
									$ADABasicOrg=$ADABasic;
									if(is_numeric($payscaleStaffProfileValue['ADAPercentage']))
									{
										$PayScaleContainerArray[$u_name]['E033']['Amount']=$this->PaygenerateRoundOff(round($ADABasic* ($payscaleStaffProfileValue['ADAPercentage']/100),2)  , $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
									}

									if(isset($SalaryMethod[$Company_id][$Location_id][$CompanyGroup]))
									{	 	
										$PayscaleDataContainerlop=array();
										$SNo++;

										$PFBasic=0;
										$PFBasicMinus=0;
										$ESIBasicStore=$ESIBasic;
										$ESIBasic=0;
										$ADABasic=0;
										$ADABasicOrg=0;
										$PFBasicArrear=0;
										$PFBasicArrearMinus=0;
										$ESIBasicArrear=0;
										$ADABasicArrear=0;

										if($PayscaleWorkerDetails[$Company_id][$Location_id][$CompanyGroup])
										{
											foreach($PayscaleWorkerDetails[$Company_id][$Location_id][$CompanyGroup] as $Mode => $ModeArray)
											{
												$AttendanceTaken=
												$AttendanceDetails[$Company_id][$CompanyGroup] [$Mode] [$u_name] ['Days'] +
												(
												(
												$AttendanceDetails[$Company_id][$CompanyGroup] [$Mode] [$u_name] ['Hours']
												+ 
												( $AttendanceDetails[$Company_id][$CompanyGroup] [$Mode] [$u_name] ['Minutes'] / 60 ) 
												)
												/ $PayscaleBasic[$Company_id][$CompanyGroup] ['Working Hours'] 
												);

												if($ModeArray['SpeMode']=='1')
												{
													// not working return 'leo';exit;
													if($ModeArray['Store'])
													{
														$WorkerSalaryTotal=0;
														if($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Earning'])
														{
															foreach($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Earning'] as $ModeIndex => $EarningAddValue)
															{
																if(is_numeric($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']))
																{
																	$WorkerSalaryTotal +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
																}
															}
														}

														if($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Allowance'])
														{
															foreach($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Allowance'] as $ModeIndex => $EarningAddValue)
															{
																if(is_numeric($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']))
																{
																	$WorkerSalaryTotal +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
																}
															}
														}

														$CalculateDays=round( $AttendanceTaken / $ModeArray['NoOfDays'], 10);

														if($AttendanceTaken && $WorkerSalaryTotal)
														$Addition=$ModeArray['Addition'];
														else
														$Addition=0;
														


														$Total=$this->PaygenerateRoundOff($WorkerSalaryTotal * $ModeArray['Percentage'] * $CalculateDays + $Addition,  $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
														
														if(is_numeric($PayscaleDataContainer['Earning'][$ModeArray['Store']]))
														{
															$PayscaleDataContainerlop['Earning'][$ModeArray['Store']]= $Total;
															$PayscaleDataContainer['Earning'][$ModeArray['Store']]=$Total;
														}

														if(is_numeric($PayscaleDataContainer['Allowance'][$ModeArray['Store']]))
														{
															$PayscaleDataContainerlop['Allowance'][$ModeArray['Store']]= $Total;
															$PayscaleDataContainer['Allowance'][$ModeArray['Store']]=$Total;
														}
													}
													else
													{
														$CalculateDays=round( $AttendanceTaken / $ModeArray['NoOfDays'], 10);
														if($AttendanceTaken)
															$Addition=$ModeArray['Addition'];
														else
															$Addition=0;

														if($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Earning'])
														{
															foreach($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Earning'] as $ModeIndex => $EarningAddValue)
															{
																if(is_numeric($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']))
																{
																	$PayscaleDataContainerlop['Earning'][$ModeIndex]=
																	$this->PaygenerateRoundOff($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']*$CalculateDays + $Addition, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
																}
															}
														}
													}
												}
												elseif($ModeArray['SpeMode']=='2' && $AttendanceDetails[$Company_id][$CompanyGroup] [$Mode] [$u_name] ['EffMonthAndYear'])
												{
													$EffMonthAndYear=$AttendanceDetails[$Company_id][$CompanyGroup] [$Mode] [$u_name] ['EffMonthAndYear'];
													//not working
													$s182=db::select("select  upper(p.u_name) 'u_name',
																		p.Name, 
																		p.Month 'Amount', p.Description,  p.SpeDescription
																		from hrm_payscale as p 
																		where p.status='1' 
																		and u_name='".$u_name."'
																		and Company='$Company'
																		and CompanyGroup='$CompanyGroup'
																		and p.data_name!='EA012' and p.data_name!='EA007' and p.data_name!='EA022' 
																		and ( '$EffMonthAndYear' BETWEEN p.`From` and if(p.`To`='','$EffMonthAndYear', p.`To`) ) 
																		order by p.company ");
													
													$PayScaleContainerArrayOld=array();
													$r=$s182;
													for($i=0;$i<count($r);$i++){
														$PayScaleContainerArrayOld[$r[$i]['u_name']] [$r[$i]['Name']]=array( 'Amount' => $r[$i]['Amount'], 'Description'=> $r[$i]['Description'], 'SpeDescription'=> $r[$i]['SpeDescription']  );
													}
													
													$WorkerADATotal=0;
													if($ModeArray['Store']){
														$WorkerSalaryTotal=0;

														foreach($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Earning'] as $ModeIndex => $EarningAddValue)
														{
															if(is_numeric($PayScaleContainerArrayOld[$u_name][$ModeIndex]['Amount']))
															{
																$WorkerSalaryTotal +=$PayScaleContainerArrayOld[$u_name][$ModeIndex]['Amount'];

																if($EarningAddValue['ADAAffected'])
																$WorkerADATotal +=$PayScaleContainerArrayOld[$u_name][$ModeIndex]['Amount'];
															}
														}

														if(is_numeric($PayScaleContainerArrayOld[$u_name]['ADAPercentage']['Description']))
														$WorkerSalaryTotal +=round($WorkerADATotal* $PayScaleContainerArrayOld[$u_name]['ADAPercentage']['Description'] / 100,2);

														$CalculateDays= round( $AttendanceTaken / $ModeArray['NoOfDays'], 10);

														if($AttendanceTaken)
															$Addition=$ModeArray['Addition'];
														else
															$Addition=0;

														$Total=$this->PaygenerateRoundOff($WorkerSalaryTotal * $ModeArray['Percentage'] * $CalculateDays + $Addition,  $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );

														$PayscaleDataContainerlop['Earning'][$ModeArray['Store']] += $Total;
														$PayscaleDataContainer['Earning'][$ModeArray['Store']] +=$Total;
													}else{
														$CalculateDays=round( $AttendanceTaken / $ModeArray['NoOfDays'], 10);

														if($AttendanceTaken)
															$Addition=$ModeArray['Addition'];
														else
															$Addition=0;

														foreach($WorkerPayrscaleSettingsArray[$Company_id][$Mode]['Earning'] as $ModeIndex => $EarningAddValue)
														{
															if(is_numeric($PayScaleContainerArrayOld[$u_name][$ModeIndex]['Amount']))
															{
																$PayscaleDataContainerlop['Earning'][$ModeIndex] +=
																$this->PaygenerateRoundOff($PayScaleContainerArrayOld[$u_name][$ModeIndex]['Amount']*$CalculateDays + $Addition, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
															}
														}
													}
												}
												elseif(!$ModeArray['SpeMode'])
												{
													$WorkerSalaryTotal=0;
													$CalculateDays= round( $AttendanceTaken / $ModeArray['NoOfDays'], 10);
													$WorkerSalaryTotal=$PayscaleWorkerActing[$Company_id][$CompanyGroup_id] [$AttendanceDetails[$Company_id][$CompanyGroup_id] [$Mode] [$u_name] ['Grade']];
													$Total=$this->PaygenerateRoundOff($WorkerSalaryTotal * $ModeArray['Percentage'] * $CalculateDays + $ModeArray['Addition'],  $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
													$PayscaleDataContainerlop['Earning'][$ModeArray['Store']]= $Total;
													$PayscaleDataContainer['Earning'][$ModeArray['Store']]=$Total;
												}
											}
										}
										
										if($PayscaleSettingArrray[$Company_id]['Earning'])
										{
											foreach($PayscaleSettingArrray[$Company_id]['Earning'] as $ModeIndex => $EarningAddValue)
											{
												if(!is_numeric($PayscaleDataContainerlop['Earning'][$ModeIndex])  and is_numeric($PayscaleDataContainer['Earning'][$ModeIndex]))
												{
													$PayscaleDataContainerlop['Earning'][$ModeIndex]=$PayscaleDataContainer['Earning'][$ModeIndex];
												}
											}
										}

										if($PayscaleSettingArrray[$Company_id]['Allowance'])
										{
											foreach($PayscaleSettingArrray[$Company_id]['Allowance'] as $ModeIndex => $EarningAddValue)
											{
												if(!is_numeric($PayscaleDataContainerlop['Allowance'][$ModeIndex])  and is_numeric($PayscaleDataContainer['Allowance'][$ModeIndex]))
												$PayscaleDataContainerlop['Allowance'][$ModeIndex]=$PayscaleDataContainer['Allowance'][$ModeIndex];
											}
										}

										$PayscaleDataContainerlop['Earning']['E033']=0;
										if($PayscaleSettingArrray[$Company_id]['Earning'])
										{
											foreach($PayscaleSettingArrray[$Company_id]['Earning'] as $ModeIndex => $EarningAddValue)
											{
												if(is_numeric($PayscaleDataContainerlop['Earning'][$ModeIndex]))
												{
													if($EarningAddValue['PFAffected'])
													{
														if($Index=='Allowance')
															$PFBasicArrear +=$PayscaleDataContainerlop['Earning'][$ModeIndex];
														else
															$PFBasic +=$PayscaleDataContainerlop['Earning'][$ModeIndex];
													}

													if($EarningAddValue['PFAffectedMinus'])
													{
														if($Index=='Allowance')
															$PFBasicArrearMinus +=$PayscaleDataContainerlop['Earning'][$ModeIndex];
														else
															$PFBasicMinus +=$PayscaleDataContainerlop['Earning'][$ModeIndex];
													}

													if($EarningAddValue['ESIAffected'])
													$ESIBasic +=$PayscaleDataContainerlop['Earning'][$ModeIndex];

													if($EarningAddValue['ADAAffected'])
													{
														$ADABasic +=$PayscaleDataContainerlop['Earning'][$ModeIndex];
														$ADABasicOrg +=	$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
													}
												}
											}
										} 

										if($PayscaleSettingArrray[$Company_id]['Allowance'])
										{
											foreach($PayscaleSettingArrray[$Company_id]['Allowance'] as $ModeIndex => $EarningAddValue)
											{
												if(is_numeric($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']))
												{
													if($EarningAddValue['PFAffected'])
													{
														if($Index=='Allowance')
															$PFBasicArrear +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
														else
															$PFBasic +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
													}

													if($EarningAddValue['PFAffectedMinus'])
													{
														if($Index=='Allowance')
															$PFBasicArrearMinus +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
														else
															$PFBasicMinus +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
													}

													if($EarningAddValue['ESIAffected'])
														$ESIBasic +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];

													if($EarningAddValue['ADAAffected'])
													{
														$ADABasic +=$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
														$ADABasicOrg +=	$PayScaleContainerArray[$u_name][$ModeIndex]['Amount'];
													}
												}
											}
										}

										$pd=$AttendanceDetails[$Company_id][$CompanyGroup]['01'][$u_name]['Days'];
										

										$nd=$AttendanceDetails[$Company_id][$CompanyGroup] ['01'] [$u_name] ['Days'];
										
										

										if(!is_numeric($pd))
										
										$pd=0;

										if(!is_numeric($nd))
										$nd=0;
										if($nd)
										$GrossSalary=round( ($TotalSalary/$nd)*$pd, 2);
										else
										$GrossSalary=0;

										$lopDetected=$this->PaygenerateRoundOff( $TotalSalary-$GrossSalary, $RoundOFFData['DATA'],  $RoundOFFData['DATADem']);
										$CalCuldatelopPercentage=1;
									}
									else #else001-start
									{
										// return 'leo working';exit;
										$lopTaken=0;
										// $pd1=db::select("aselect emp_code,MonthAndYear,Days AS PD,total_work_days
										// 					from hrm_lop where MonthAndYear= '".$MonthAndYear."' and emp_code='".$empno."' ");

										$pd1=db::select("select emp_code,MonthAndYear,Days AS PD,total_work_days
															from hrm_lop where MonthAndYear= '".$MonthAndYear."'");
				 
										$pd2=json_decode(json_encode($pd1), true);
										foreach ($pd2 as $paid => $days) {
											// $pd = $days['PD'] - $days['total_work_days'];
											$pd = $days['total_work_days'] - $days['PD'];
										}

										$old_lop1=db::select("select emp_code,MonthAndYear,old_lop AS PD,total_work_days
															from hrm_lop where MonthAndYear= '".$MonthAndYear."'");
										$old_lop2=json_decode(json_encode($old_lop1), true);
										foreach ($old_lop2 as $paid => $days) {
											$pd = $days['total_work_days'] - $days['PD'];
										}

										$new_lop1=db::select("select emp_code,MonthAndYear,new_lop AS PD,total_work_days
															from hrm_lop where MonthAndYear= '".$MonthAndYear."'");
										$new_lop2=json_decode(json_encode($new_lop1), true);
										foreach ($new_lop2 as $paid => $days) {
											$pd = $days['total_work_days'] - $days['PD'];
										}
										
										$SNo++;
										$GrossSalary=round(($TotalSalary/$nd)*$pd, 10);
										$lopDetected=$this->PaygenerateRoundOff( $TotalSalary-$GrossSalary, $RoundOFFData['DATA'],  $RoundOFFData['DATADem']);
										// note 1 return $lopDetected;exit;	
										
										$CalCuldatelopPercentage=0;
										
										if($GrossSalary)
											$CalCuldatelopPercentage=round($GrossSalary/$TotalSalary, 10 );
										else
											$CalCuldatelopPercentage=0;

										$ExtraDays=$ExtraSalaryPercentage=0;
										if(isset($AttendanceDetails[$Company_id][$CompanyGroup_id] ['52'] [$u_name] ['Days']))
										$ExtraDays=$AttendanceDetails[$Company_id][$CompanyGroup_id] ['52'] [$u_name] ['Days'];

										if($ExtraDays)
										{
											$ExtraSalary=round( ($TotalSalary/$AttendanceDetails[$Company_id][$CompanyGroup_id] ['52'] [$u_name] ['TotalDays'])*$ExtraDays, 2);

											$ExtraSalaryPercentage=round($ExtraSalary/$TotalSalary, 10 );
										
											foreach($WorkerPayrscaleSettingsArray[$Company_id]['52']['Earning']  as $ModeIndex => $EarningAddValue)
											{
												if(is_numeric($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']))
												{
													if($EarningAddValue['PFAffected'])
														$PFBasicArrear +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $ExtraSalaryPercentage, 10 );
													if($EarningAddValue['PFAffectedMinus'])
														$PFBasicArrearMinus +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $ExtraSalaryPercentage, 10 );
													if($EarningAddValue['ESIAffected'])
														$ESIBasicArrear +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $ExtraSalaryPercentage, 10 );
													if($EarningAddValue['ADAAffected'])
														$ADABasicArrear +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $ExtraSalaryPercentage, 10 );
												}
											}
										}

										$Holidays=$HolidaySalaryPercentage=0;
										if(isset($AttendanceDetails[$Company_id][$CompanyGroup_id] ['51'] [$u_name] ['Days']))
											$Holidays=$AttendanceDetails[$Company_id][$CompanyGroup_id] ['51'] [$u_name] ['Days'];

										if($Holidays)
										{
											$HolidaySalary=round( ($TotalSalary/$AttendanceDetails[$Company_id][$CompanyGroup_id] ['51'] [$u_name] ['TotalDays'])*$Holidays, 2);

											$HolidaySalaryPercentage=round($HolidaySalary/$TotalSalary, 10 ); 
											foreach($WorkerPayrscaleSettingsArray[$Company_id]['51']['Earning']  as $ModeIndex => $EarningAddValue)
											{
												if(is_numeric($PayScaleContainerArray[$u_name][$ModeIndex]['Amount']))
												{
													if($EarningAddValue['PFAffected'])
														$PFBasicArrear +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $HolidaySalaryPercentage, 10 );
													if($EarningAddValue['PFAffectedMinus'])
														$PFBasicArrearMinus +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $HolidaySalaryPercentage, 10 );
													if($EarningAddValue['ESIAffected'])
														$ESIBasicArrear +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $HolidaySalaryPercentage, 10 );
													if($EarningAddValue['ADAAffected'])
														$ADABasicArrear +=round($PayScaleContainerArray[$u_name][$ModeIndex]['Amount'] * $HolidaySalaryPercentage, 10 );
												}
											}
										}
										
										
										$PayscaleDataContainerlop=array();
										foreach($PayscaleDataContainer['Earning'] as $Index => $EarningAddValue)
										{
											$HolidaySalary=0;
											if(isset($WorkerPayrscaleSettingsArray[$Company_id]['51']['Earning'][$Index] ))
											$HolidaySalary=$this->PaygenerateRoundOff($EarningAddValue*$HolidaySalaryPercentage, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );

											if($Index=='E065'){
												$PayscaleDataContainerlop['Earning'][$Index]=
												$this->PaygenerateRoundOff(round($EarningAddValue*$CalCuldatelopPercentage,0), $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] ) + 
												$this->PaygenerateRoundOff(round($EarningAddValue*$ExtraSalaryPercentage,0), $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] )  +
												$HolidaySalary;
											}else{
												$PayscaleDataContainerlop['Earning'][$Index]=
												$this->PaygenerateRoundOff($EarningAddValue*$CalCuldatelopPercentage, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] ) + 
												$this->PaygenerateRoundOff($EarningAddValue*$ExtraSalaryPercentage, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] )  +
												$HolidaySalary;
											}
										}

										if(isset($PayscaleDataContainer['Allowance']))
										{
											foreach($PayscaleDataContainer['Allowance'] as $Index => $EarningAddValue)
											{
												$PayscaleDataContainerlop['Allowance'][$Index]=$this->PaygenerateRoundOff($EarningAddValue, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
											}
										}
									} #elseend001

									//return 'rolex';exit;
									if(array_sum($PayscaleDataContainerlop['Earning']))
										$SpecialEarningTotal=array_sum($PayscaleDataContainerlop['Earning']);
									else
										$SpecialEarningTotal=0;

									//Employee ADA Start
									$ADAThisMonthOnly=0;
									$ADAPreMonthOnly=0;
									$ADA=0;
									$ADAOrg=0;
									
									if($payscaleStaffProfileValue['ADAPercentage'] && is_numeric($payscaleStaffProfileValue['ADAPercentage']))
									{
										$ADAOrg=$this->PaygenerateRoundOff(round($ADABasicOrg* ($payscaleStaffProfileValue['ADAPercentage']/100),2)  , $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
										$ADABasicAffected=round( $ADABasic*$CalCuldatelopPercentage, 2) + $ADABasicArrear;
											
										$ADAThisMonthOnly=$this->PaygenerateRoundOff(round($ADABasicAffected* ($payscaleStaffProfileValue['ADAPercentage']/100),2)  , $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
										$ADA=$ADAThisMonthOnly+$ADAPreMonthOnly;
									}
									//Employee ADA Ended

									//Employee PF Started
									$PFBasicAffected=0;
									$PFBasicAffectedMinus=0;
									$PFBasicSalaryArrear=0;
									$PFBasicSalaryArrearMinus=0;

									$EePFThisMonthOnly=0;
									$EePFPreMonthOnly=0;
									$EePF=0;

									$EeVPFThisMonthOnly=0;
									$EeVPFPreMonthOnly=0;
									$EeVPF=0;

									$ErPFThisMonthOnly=0;
									$ErPFPreMonthOnly=0;
									$ErPF=0;

									$ErPenstionThisMonthOnly=0;
									$ErPenstionPreMonthOnly=0;
									$ErPenstion=0;
									$PFCalculation=0;

									if($payscaleStaffProfileValue['PFCalculation'])
									{
										if(isset($SalaryMethod[$Company_id][$Location_id][$CompanyGroup_id])){
											$PFBasic +=$ADAThisMonthOnly; 
											$PFBasicMinus +=$ADAThisMonthOnly; 
										}else{
											$PFBasic +=$ADAOrg;
											$PFBasicMinus +=$ADAOrg;
										}
										
										$PFBasicActualValue =$PFBasic +$PFBasicArrear;
										$PFBasicActualMinusValue =$PFBasicMinus +$PFBasicArrearMinus;
										$PFBasicAffected=round( $PFBasic*$CalCuldatelopPercentage, 2);
										$PFBasicAffectedMinus=round( $PFBasicMinus*$CalCuldatelopPercentage, 2);
										
										if($payscaleStaffProfileValue['PFCalculation']=='5' )
										{ 
											if(($PFBasicMinus*$CalCuldatelopPercentage)>=15000){
												$PFBasicAffected=$PF_Limit;
											}else{
												$PFBasicAffected=($PFBasicMinus*$CalCuldatelopPercentage);
											}
										}	

										if($payscaleStaffProfileValue['PFCalculation']=='4')
										{ 	
											if($PFBasic < $PF_Limit)
											{
												if($PFBasicMinus > $PF_Limit){
													if($PFBasicAffectedMinus > $PF_Limit)
														$PFBasicAffected=$PF_Limit;
													else
														$PFBasicAffected=$PFBasicAffectedMinus;
												}else{
													$PFBasicAffected=$PFBasicAffectedMinus;
												}	
											}

											if(is_numeric($payscaleStaffProfileValue['FixedPFAmount']) && $payscaleStaffProfileValue['FixedPFAmount']>0)
											{
												if($PFBasicAffected > $payscaleStaffProfileValue['FixedPFAmount'] ) 
													$PFBasicAffected = $payscaleStaffProfileValue['FixedPFAmount'];
											}
										}

										$PFBasicAffected +=$PFBasicArrear;

										if($payscaleStaffProfileValue['PFCalculation']=='2')
										{
											if(is_numeric($payscaleStaffProfileValue['FixedPFAmount']))
											{
												if($PFBasicAffected > $payscaleStaffProfileValue['FixedPFAmount'] ) 
												$PFBasicAffected = $payscaleStaffProfileValue['FixedPFAmount'];
											}
										}

										if($payscaleStaffProfileValue['PFCalculation']=='3')
										{
											if(is_numeric($payscaleStaffProfileValue['FixedPFAmount']))
											$PFBasicAffected = round( $payscaleStaffProfileValue['FixedPFAmount'] * $CalCuldatelopPercentage, 2); // $payscaleStaffProfileValue['FixedPFAmount'];
										}

										$PFBasicAffected=$this->PaygenerateRoundOff($PFBasicAffected,$RoundOFFData['PFBasic'], $RoundOFFData['PFBasicDem'] );
										$EePFThisMonthOnly=$this->PaygenerateRoundOff(round($PFBasicAffected*$pf_per,2), $RoundOFFData['PF'], $RoundOFFData['PFDem'] );
										$EePF=$EePFThisMonthOnly+$EePFPreMonthOnly;

										if(is_numeric($payscaleStaffProfileValue['VPFPercentage']) && $payscaleStaffProfileValue['VPFPercentage']>0)
										{
											$EeVPFThisMonthOnly=
											$this->PaygenerateRoundOff(round($PFBasicAffected* ($payscaleStaffProfileValue['VPFPercentage']/100),2),$RoundOFFData['PF'], $RoundOFFData['PFDem'] );
											$EeVPF=$EeVPFThisMonthOnly+$EeVPFPreMonthOnly;
										}
										
										$ErPFThisMonthOnly=$this->PaygenerateRoundOff(($ErPFPer * $PFBasicAffected),$RoundOFFData['PF'], $RoundOFFData['PFDem'] );
										$ErPenstionThisMonthOnly=$this->PaygenerateRoundOff(($ErPensionPer*$PFBasicAffected),$RoundOFFData['PF'], $RoundOFFData['PFDem'] );
									
										if($PFBasicAffected > $ErPensionMax){
											$ErPFThisMonthOnly += $ErPenstionThisMonthOnly - ( 
											$this->PaygenerateRoundOff(($ErPensionPer*$ErPensionMax),$RoundOFFData['PF'], $RoundOFFData['PFDem'] ) );
											$ErPenstionThisMonthOnly = $this->PaygenerateRoundOff(($ErPensionPer*$ErPensionMax),$RoundOFFData['PF'], $RoundOFFData['PFDem'] );
											$EPSSoruceValue= $ErPensionMax;
										}else{	
											$EPSSoruceValue= $this->PaygenerateRoundOff( $PFBasicAffected, $RoundOFFData['DATA'], $RoundOFFData['DATADem']) ; 
										}

										$ErPF=$ErPFThisMonthOnly+$ErPFPreMonthOnly;
										$ErPenstion=$ErPenstionThisMonthOnly+$ErPenstionPreMonthOnly;

										if($EePF != ($ErPF+$ErPenstion))
											$ErPF += $EePF - ($ErPF+$ErPenstion);
										
										if(!$StaffEPSActive){
											$ErPF +=$ErPenstion;
											$ErPenstion=0;
										}

										$PFArreaCalculation=0;
										$InsertQuery='';
										
										if((!empty($PayscaleDataContainerlop['Allowance']['EA003'])) || (!empty($PayscaleDataContainerlop['Earning']['E016'] ))){
											$PFArreaCalculation=!empty($PayscaleDataContainerlop['Allowance']['EA003']) + !empty($PayscaleDataContainerlop['Earning']['E016']);
										}
										

										if(isset($PayscaleDataContainerlop['Allowance']['EA001']))
											$PayscaleDataContainerlop['Allowance']['EA001']=round($PayscaleDataContainerlop['Allowance']['EA001']);

										if(!empty($PFArreaCalculation))
										{
											unset($ArrearArray);
											$ArrearArray=$this->PFCalculation($PFArreaCalculation,$payscaleStaffProfileValue, $RoundOFFData, $pf_per,
											$ErPFPer, $ErPensionPer , $ErPensionMax-$EPSSoruceValue );

											if(!is_numeric($ArrearArray[0]))
												$ArrearArray[0]=0;
											if(!is_numeric($ArrearArray[1]))
												$ArrearArray[1]=0;
											if(!is_numeric($ArrearArray[2]))
												$ArrearArray[2]=0;
											if(!is_numeric($ArrearArray[3]))
												$ArrearArray[3]=0;
											if(!is_numeric($ArrearArray[4]))
												$ArrearArray[4]=0;

											$InsertQuery = db::insert("
											insert into hrm_payscale_monpayr_arrear ( MonthAndYear, EffMonthAndYear, u_name, company_id, location_id, payroll_group_id, category_of_emp,DataName, `Values`, description ) 
											values 
											( '".$MonthAndYear."', '".$MonthAndYear."', '".$u_name."', '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."', '".$CategoryOfEmp."',
											'PFBasicSalary', '".$ArrearArray[0]."', 'Arrear Calculation'),

											( '".$MonthAndYear."', '".$MonthAndYear."', '".$u_name."', '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."', '".$CategoryOfEmp."',
											'D001', '".$ArrearArray[1]."', 'Arrear Calculation'),

											( '".$MonthAndYear."', '".$MonthAndYear."', '".$u_name."', '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."', '".$CategoryOfEmp."',
											'D003', '".$ArrearArray[2]."', 'Arrear Calculation'),

											( '".$MonthAndYear."', '".$MonthAndYear."', '".$u_name."', '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."', '".$CategoryOfEmp."',
											'D004', '".$ArrearArray[3]."', 'Arrear Calculation'),

											( '".$MonthAndYear."', '".$MonthAndYear."', '".$u_name."', '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."', '".$CategoryOfEmp."',
											'EPSSoruce', '".$ArrearArray[4]."', 'Arrear Calculation')

											");
										}
									}

									$Gross=$GrossSalary;

									//Employee ESI Started
									$EeESIThisMonthOnly=0.00;
									$EeESIPreMonthOnly=0;
									$EeESI=0;
									$ErESIThisMonthOnly=0;
									$ErESIPreMonthOnly=0;
									$ErESI=0;
								
									if($payscaleStaffProfileValue['ESICalculation'])
									{
										$ESIBasicAffected=round( $ESIBasic*$CalCuldatelopPercentage, 2) + $ESIBasicArrear;
										
										if($payscaleStaffProfileValue['ESICalculation'] =='1')
										{
											$ESIBasicStoreEligible=$GrossSalaryForESI;

											if($ESIBasicStoreEligible <= $ESIEligible )
											{
												(float)$dd=(float)$ESIBasicAffected*(float)$esi_per;

												$ddd=round((float)$dd,2);
												
												$EeESIThisMonthOnly=(float)($this->PaygenerateRoundOff($ddd,$RoundOFFData['ESI'],$RoundOFFData['ESIDem'] ));
												$EeESI=$EeESIThisMonthOnly+$EeESIPreMonthOnly;
											
												$ErESIThisMonthOnly=$this->PaygenerateRoundOff(round($ESIBasicAffected*$esi_per_o,2)  , $RoundOFFData['ESI'],  $RoundOFFData['ESIDem'] );
												$ErESI=$ErESIThisMonthOnly+$ErESIPreMonthOnly;
											}
										}
										else if($payscaleStaffProfileValue['ESICalculation'] ==2)
										{
											$EeESIThisMonthOnly=$this->PaygenerateRoundOff(round($ESIBasicAffected*$esi_per,2)  , $RoundOFFData['ESI'],  $RoundOFFData['ESIDem'] );
											$EeESI=$EeESIThisMonthOnly+$EeESIPreMonthOnly;
											
											$ErESIThisMonthOnly=$this->PaygenerateRoundOff(round($ESIBasicAffected*$esi_per_o,2)  , $RoundOFFData['ESI'],  $RoundOFFData['ESIDem'] );
											$ErESI=$ErESIThisMonthOnly+$ErESIPreMonthOnly;
										}
									}


									if(isset($PayscaleDataContainerlop['Allowance']['EA004']))
									{
										if(is_numeric($PayscaleDataContainerlop['Allowance']['EA004']))
										{
											$PayscaleDataContainerlop['Allowance']['EA004'] *= round((round($pd/$nd)+1)/2,1) ;
											
										}
									}

									$TotalEarning  = 0;	
									if(isset($PayscaleDataContainerlop['Allowance']))
									{
										if($PayscaleDataContainerlop['Allowance'])
											$TotalEarning=array_sum($PayscaleDataContainerlop['Allowance']);
										else
											$TotalEarning=0;
									}

									$TotalEarning = $this->PaygenerateRoundOff($TotalEarning, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );

									$Gross +=$TotalEarning ;
									
									$Gross=$this->PaygenerateRoundOff($Gross, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
									{
										$D007=$PayscaleDataContainer['Deduction']['D007'];
										if(!is_numeric($D007))
										$D007=0;
										
										$D008=$PayscaleDataContainer['Deduction']['D008'];
										if(!is_numeric($D008))
											$D008=0;

										if(!$D008){
											if($IncomeShow)
												$D008 =$this->PaygenerateRoundOff($Gross* $IncomeTaxPercentage, $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
										}

										if(!is_numeric($D008))
										$D008=0;
									}

									/*cunsultant it */
									if($Emp_Type=='5'){
										$D008 =round((($Gross * 10)/100),0);
									}

									
									$TotalDeduction=0;
									if($PayscaleDataContainer['Deduction'])
									{
										foreach($PayscaleDataContainer['Deduction'] as $Index => $EarningAddValue)
										{
											if(is_numeric($EarningAddValue))
											{
												$PayscaleDataContainer['Deduction'][$Index] =$this->PaygenerateRoundOff( $EarningAddValue , $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );
											}
										}
									}

									{
										$ExtraData='';

										if($AGE>=58){
											$ErPF +=$ErPenstion;
											$ErPenstion=0;	
											$EPSSoruceValue=0;
										}

										$PayscaleDataContainer['Earning']['E033']=$ADAOrg;
										$PayscaleDataContainerlop['Earning']['E033']=$ADA;

										
										$TotalEarnings=$TotalEarningsActual=0;
										if($PayscaleDataContainer['Earning'])
										{
											foreach($PayscaleDataContainer['Earning'] as $Index => $EarningAddValue)
											{
												if($Index=='E067' || $Index=='E075' || $Index=='E076' || $Index=='E077' && $EarningAddValue!='0' )
												{	
													$ExtraData .="
													(
													'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', '".$Index."','".$PayscaleDataContainerlop['Earning'][$Index]."', '0', '".$PayscaleDataContainerlop['Earning'][$Index]."', '0', 'Calculate', '','".$preActive."'
													), ";

													if(isset($PayscaleSettingArrray[$Company_id]['Earning'][$Index]['Ee']))
													{
														if($PayscaleSettingArrray[$Company_id]['Earning'][$Index]['Ee'])
														{
															$TotalEarnings +=$PayscaleDataContainerlop['Earning'][$Index];
															$TotalEarningsActual +=$EarningAddValue;
															$ctcvalue+=$PayscaleDataContainerlop['Earning'][$Index];
															$ctcActual+=$EarningAddValue;
														}
													}
												}

												if($EarningAddValue> 0)
												{
													$ExtraData .="
													(
													'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', '".$Index."','".$PayscaleDataContainerlop['Earning'][$Index]."', '".$EarningAddValue."', '".$PayscaleDataContainerlop['Earning'][$Index]."', '0', 'Calculate', '','".$preActive."'
													), ";

													if(isset($PayscaleSettingArrray[$Company_id]['Earning'][$Index]['Ee']))
													{
														if($PayscaleSettingArrray[$Company_id]['Earning'][$Index]['Ee'])
														{
															$TotalEarnings +=$PayscaleDataContainerlop['Earning'][$Index];
															$TotalEarningsActual +=$EarningAddValue;
															$ctcvalue+=$PayscaleDataContainerlop['Earning'][$Index];
															$ctcActual+=$EarningAddValue;
														}
													}
												}
											}
										}

										if(isset($PayscaleDataContainer['Allowance']))
										{
											foreach($PayscaleDataContainer['Allowance'] as $Index => $EarningAddValue)
											{
												if($EarningAddValue> 0)
												{
													if(!isset($PayScaleContainerArray[$u_name][$Index]['Description']))
													$PayScaleContainerArray[$u_name][$Index]['Description'];

													$ExtraData .="
													(
													'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', '".$Index."','".$PayscaleDataContainerlop['Allowance'][$Index]."', '".round($EarningAddValue)."', '".$PayscaleDataContainerlop['Allowance'][$Index]."', '0', '".$PayScaleContainerArray[$u_name][$Index]['Description']."', '','".$preActive."'
													), ";

													if($PayscaleSettingArrray[$Company_id]['Allowance'][$Index]['Ee'])
													{
														$TotalEarnings +=$PayscaleDataContainerlop['Allowance'][$Index];
														$TotalEarningsActual +=$EarningAddValue;
														$ctcvalue +=$PayscaleDataContainerlop['Allowance'][$Index];
														$ctcActual+=round($EarningAddValue);
													}
												}
											}
										}
										
										$TotalDeductions=0;
										if($PayscaleDataContainer['Deduction'])
										{
											foreach($PayscaleDataContainer['Deduction'] as $Index => $EarningAddValue)
											{
												if($EarningAddValue> 0)
												{
													if(!isset($PayScaleContainerArray[$u_name][$Index]['SpeDescription']))
													$PayScaleContainerArray[$u_name][$Index]['SpeDescription'];

													$ExtraData .="
													(
													'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', '".$Index."','".$EarningAddValue."', '".$EarningAddValue."', '".$EarningAddValue."', '0', 'Calculate', '".$PayScaleContainerArray[$u_name][$Index]['SpeDescription']."','".$preActive."'
													), ";

													$ctcvalue +=$EarningAddValue;
													$ctcActual+=$EarningAddValue;

													if($PayscaleSettingArrray[$Company_id]['Deduction'][$Index]['Ee'])
													{
														$TotalDeductions +=$EarningAddValue;
													}
												}
											}
										}
										
										$Gross=$TotalEarnings;

										$Gross_Actual=$TotalEarningsActual;										
										$TotalDeduction = $this->PaygenerateRoundOff( $TotalDeductions , $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] ); // Because this is Given by Eployer
										$NetSalary=$this->PaygenerateRoundOff( ($Gross-$TotalDeduction ), $RoundOFFData['DATA'],  $RoundOFFData['DATADem'] );

										$RoundOff=0;
										if($RoundOFFData['NetRoundOff'])
										{
											$RoundOff=round($Gross - $TotalDeduction ,0);
											$RoundOff =( $RoundOff + $TotalDeduction ) - $Gross;
										}
									}
								}
								else
								{
									if(!$preActive)
									$ZeroSalary++;

									$SNo++;
									$TotalSalary=$Gross=$TotalDeduction=$NetSalary=$Gross_Actual=0;

									
								}

								if(!$DOR)
								$DOR='0000-00-00';

								$lophour=$lop_deduction=$lopAmount=0;

								
										
									
								$s0N=db::insert("insert into hrm_payscale_monpayr_details
												(
													MonthAndYear, u_name, EmpNo, Name, FatherName, company_id, location_id,division_id, payroll_group_id,category_of_emp, WorkLocation,  dept, 
													designation, dob, doj, DOR, Active, preActive, gender,
													CompanyPFNo, EmpESINO, EmpPFNO, CostCodeName, PANNo, BankAcNo, BankName,BankIFSC, VPFPer, SlabName, GradeName, ESICalculation, PFCalculation, 
													lopAmountAmount, lopHourAmount, lopHour, lopAmount, PD, WD, UAN,off_mail_id,payslip_model
												) values
												(
													'".$MonthAndYear."', '".$u_name."', '".$empno."', '".$name."',  '".$father_name."', '".$Company_id."', '".$Location_id."', '".$division."', '".$CompanyGroup_id."','".$CategoryOfEmp."', '".$payscaleStaffProfileValue['work_location']."', 
													'".$dept."',	'".$designation."',	'".$dob."', '".$doj."','".$DOR."',  '".$Active."', '".$preActive."', '".$gender."',
													'".$payscaleStaffProfileValue['CompanyPFNo']."', '".$payscaleStaffProfileValue['EmpESINO']."', '".$payscaleStaffProfileValue['EmpPFNO']."', 
													'".$payscaleStaffProfileValue['CostCodeName']."',  '".$payscaleStaffProfileValue['PANNo']."',  '".$payscaleStaffProfileValue['BankAcNo']."',  
													'".$payscaleStaffProfileValue['BankName']."',  '".$payscaleStaffProfileValue['BankIFSC']."', '".$payscaleStaffProfileValue['VPFPercentage']."',  '".$payscaleStaffProfileValue['SlabName']."',  
													'".$payscaleStaffProfileValue['GradeName']."', '".$payscaleStaffProfileValue['ESICalculation']."', '".$payscaleStaffProfileValue['PFCalculation']."', 
													'".number_format($lopDetected,0,".","")."', '".number_format($lophour,0,".","")."', '".number_format($lop_deduction,0,".","")."', 
													'".number_format($lopAmount,0,".","")."', '".number_format($pd,2)."', '".number_format($nd,2)."', '".$UAN."', 
													'".$payscaleStaffProfileValue['office_mail_id']."', '".$PaySlipModel."'
												)");

										
								
								if($payscaleStaffProfileValue['preActive']==2)
								{
									$payscale_hold_delete=DB::delete("delete from `hrm_monpayr_hold` where emp_code= '".$u_name."' and monthandyear='".$MonthAndYear."' and payroll_group_id= '".$CompanyGroup_id."'");
									$payscale_hold=DB::insert("INSERT INTO `hrm_monpayr_hold` (`company_id`, `payroll_group_id`, `emp_code`, `monthandyear`, `net`, `gross`,deduction, `release_monthandyear`, `status`) VALUES ( '".$Company_id."', '".$CompanyGroup_id."', '".$u_name."','".$MonthAndYear."','".$NetSalary."', '".$Gross."','".$TotalDeduction."',null, 1)");				 
								}

								$getLtaAmt=db::select("select  upper(p.u_name) 'u_name',
														p.data_name 'Name', 
														p.monthly_value 'Amount',p.yearly_value, p.Description,p.SpeDescription
														from hrm_payscale as p 
														where p.status='1' 
														and u_name='".$u_name."'
														and company_id='".$Company_id."'
														and payroll_group_id='".$CompanyGroup_id."'
														and ( '".$MonthAndYear."' BETWEEN p.`From` and if(p.`To`='','".$MonthAndYear."', p.`To`) ) and p.data_name in ('EA007') 
														order by p.company_id ");
								$getLtaAmt=json_decode(json_encode($getLtaAmt), true);

								$explode_month=explode("-",$MonthAndYear);
								$total_days_in_month=cal_days_in_month(CAL_GREGORIAN,$explode_month[1],$explode_month[0]);

								//$lta_earned_amount=($getLtaAmt['0']['Amount']/$total_days_in_month)*$pd;
								$lta_earned_amount=($getLtaAmt['0']['yearly_value']/365)*$pd;

								if(!empty($getLtaAmt)){
									$insertLTA=DB::insert("2INSERT INTO `hrm_payscale_monpayr` (`MonthAndYear`, `u_name`, `company_id`, `location_id`,`payroll_group_id`, 
															`category_of_emp`, `DataName`, `payable`, `Description`, `SpeDescription`, `preActive`) values 
															('".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', 'EA007',
															'".$lta_earned_amount."','','','".$preActive."')");
								}

								$sqlins ="insert into hrm_payscale_monpayr(
								MonthAndYear, u_name, company_id, location_id, payroll_group_id,category_of_emp, DataName, `Values`, Actual, Pre, Per, Description, SpeDescription,preActive
								) values ";
								
								$MealdeductionSMS=$PayScaleContainerArray[$u_name]['E065']['Amount'];
								$NPSdeductionSMS=$PayScaleContainerArray[$u_name]['E066']['Amount'];
								$getActual_gross=$PayScaleContainerArray[$u_name]['Gross']['Amount'];
								{

									$sqlins .=
									"
									(
									'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."', '".$CategoryOfEmp."','TotalSalary','".$TotalSalary."', '0', '0', '0', 'Calculate', '','".$preActive."'
									),

									(
									'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', 'CTC','".$ctcvalue."','".$ctcActual."',  '".$ctcvalue."', '0', 'Calculate', '','".$preActive."'
									),
									".$ExtraData."
									(

									'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', 'Gross','".$Gross."', '".$Gross_Actual."', '".$Gross."', '0', 'Calculate', '','".$preActive."'
									),
									(
									'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', 'Net','".$NetSalary."', '0', '0', '0', 'Calculate', '','".$preActive."'
									)";

									if($RoundOff>0)
									{
										$sqlins .=",
										(
										'".$MonthAndYear."', '".$u_name."',  '".$Company_id."', '".$Location_id."', '".$CompanyGroup_id."','".$CategoryOfEmp."', 'E000','".$RoundOff."', '".$RoundOff."', '0', '0', 'Calculate', '','".$preActive."'
										)";
									}
								}
								
								$sqlins=db::insert($sqlins);

								if($InsertQuery)
								{
								
								}

								// Count calculation moved to earlier in the code for proper display
							}
						}
						
						foreach($IncrementArray as $Increment)
						$e=explode("-", $MonthAndYear);
						$result=array();
						$data='success';
						$result=array('company'=>$Company,'CompanyGroup'=>$getPayGrpName[0]->group,'monthyear'=>date('F - Y', mktime(0,0,0, $e[1], 1, $e[0])),'ActiveList'=>$ActiveList,'HoldList'=>$HoldList,'ZeroSalaryList'=>$ZeroSalaryList,'Employee'=>$EmployeeList,'data'=>$data,'endtime'=>date("d-m-Y H:i:s"),'activelist'=>$activelist,'zerolist'=>$zerolist,'holdlist'=>$holdlist,'notification'=>$Notification,'Error'=>$Error,'IT'=>$curMonthTaxArray,'status'=>true);
						
						return $result;
					}
					else
					{
						$data='No Structure';

						$e=explode("-", $MonthAndYear);
						$result=array('company'=>$Company,'CompanyGroup'=>$CompanyGroup,'monthyear'=>date('F - Y', mktime(0,0,0, $e[1], 1, $e[0])),'data'=>$data,'info'=>"No Employee's Salary Structure Found for Generating Salary ",'endtime'=>date("d-m-Y H:i:s"));
						return $result;
						echo "<p align=center>
						<table align=center class='table table-striped table-bordered' >
						<tr><th align=left>Company Name </th><td>".$Company."</td></tr>

						<tr><th align=left>Company Groups </th><td>".$CompanyGroup."</td></tr>
						<tr><th align=left>Month and Year </th><td>".date('F - Y', mktime(0,0,0, $e[1], 1, $e[0]))."</td></tr>
						<tr><th align=left>Status </th><td><font color=red size=+2> No Employee's Salary Structure Found for Generating Salary </font></td></tr>
						</table></p>";
					}
				}
				else
				{
					$data='No Profile';

					$e=explode("-", $MonthAndYear);
					$result=array('company'=>$Company,'CompanyGroup'=>$CompanyGroup,'monthyear'=>date('F - Y', mktime(0,0,0, $e[1], 1, $e[0])),'data'=>$data,'info'=>"No Employee's Profile Found For Salary Generate ",'endtime'=>date("d-m-Y H:i:s"));
					return $result;
					echo "<p align=center>
					<table align=center class='table table-striped table-bordered' >
					<tr><th align=left>Company Name </th><td>".$Company."</td></tr>

					<tr><th align=left>Company Groups </th><td>".$CompanyGroup."</td></tr>
					<tr><th align=left>Month and Year </th><td>".date('F - Y', mktime(0,0,0, $e[1], 1, $e[0]))."</td></tr>
					<tr><th align=left>Status </th><td><font color=red size=+2> No Employee's Profile Found For Salary Generate </font></td></tr>
					</table></p>";
				}

				echo "<center> <font color=#000000 size=+1> End Time : ".date("d-m-Y H:i:s")."</font><br></center>";
			}
			else
			{
				$data='open month';
				$generateArray['data']=$data;
				$generateArray['info']= '
				Information! 
				Please Open Month For Salary Process
				';
				return $generateArray;
			}
		}
		else
		{
			$data='open month';
			$generateArray['data']=$data;
			$generateArray['info']= '
			Information! 
			Please Open Month For Salary Process
			';
			return $generateArray;
		}
	}
	/*Payroll generate end */

    ?>